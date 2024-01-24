from numpy import ndarray
import numpy as np
import operator
from unit import dim as dims, conv, idim
from unitparse import (eval_units as unit_parse, 
                      linadd as d_add, 
                      linsubtract as d_sub, 
                      linscale as d_scale)
from utils import prec_round

class UnknownUnitError(KeyError):
    def __init__(self,msg):
        KeyError.__init__(self, msg)

class DimensionMismatchError(Exception):
    """
    Exception class for attempted operations with inconsistent dimensions.

    For example, ``3*mvolt + 2*amp`` raises this exception. The purpose of this
    class is to help catch errors based on incorrect units. The exception will
    print a representation of the dimensions of the two inconsistent objects
    that were operated on.

    Parameters
    ----------
    description : ``str``
        A description of the type of operation being performed, e.g. Addition,
        Multiplication, etc.
    dims : `Dimension`
        The physical dimensions of the objects involved in the operation, any
        number of them is possible
    """
    def __init__(self, description, *objs):
        # Call the base class constructor to make Exception pickable, see:
        # http://bugs.python.org/issue1692335
        Exception.__init__(self, description, *objs)
        self.objs = objs
        self.desc = description

    def __repr__(self):
        dims_repr = [repr(obj.dim) for obj in self.objs]
        return '%s(%r, %s)' % (self.__class__.__name__,
                               self.desc, ', '.join(dims_repr))

    def __str__(self):
        s = self.desc
        if len(self.objs) == 0:
            pass
        elif len(self.objs) == 1:
            s += ' (unit is ' + '*'.join(f'{k}^{v}' for k, v in self.objs[0].units.items() if abs(v) > 0) 
        elif len(self.objs) == 2:
            d1, d2 = self.dims
            s += ' (units are {} and {}'.format('*'.join(f'{k}^{v}' for k, v in self.objs[0].units.items() if abs(v) > 0),
                    '*'.join(f'{k}^{v}' for k, v in self.objs[1].units.items() if abs(v) > 0))
#        else: #all operations are binary
#            s += (' (units are ' +
#                  ' '.join(['(' + get_unit_for_display(d) + ')'
#                            for d in self.dims]))
        if len(self.objs):
            s += ').'
        return s

def is_scalar_type(obj):
    """
    Tells you if the object is a 1d number type.

    Parameters
    ----------
    obj : `object`
        The object to check.

    Returns
    -------
    scalar : `bool`
        ``True`` if `obj` is a scalar that can be interpreted as a
        dimensionless `Quantity`.
    """
    try:
        return obj.ndim == 0
    except AttributeError:
        return np.isscalar(obj) and not isinstance(obj, str)


def fail_for_dimension_mismatch(obj1, obj2=None, error_message=None,
                                **error_quantities):
    '''
    Compare the dimensions of two objects.

    Parameters
    ----------
    obj1, obj2 : {array-like, `Quantity`}
        The object to compare. If `obj2` is ``None``, assume it to be
        dimensionless
    error_message : str, optional
        An error message that is used in the DimensionMismatchError
    error_quantities : dict mapping str to `Quantity`, optional
        Quantities in this dictionary will be converted using the `_short_str`
        helper method and inserted into the ``error_message`` (which should
        have placeholders with the corresponding names). The reason for doing
        this in a somewhat complicated way instead of directly including all the
        details in ``error_messsage`` is that converting large quantity arrays
        to strings can be rather costly and we don't want to do it if no error
        occured.

    Returns
    -------
    dim1, dim2 : `Dimension`, `Dimension`
        The physical dimensions of the two arguments (so that later code does
        not need to get the dimensions again).

    Raises
    ------
    DimensionMismatchError
        If the dimensions of `obj1` and `obj2` do not match (or, if `obj2` is
        ``None``, in case `obj1` is not dimensionsless).

    Notes
    -----
    Implements special checking for ``0``, treating it as having "any
    dimensions".
    '''

    o1hasdim = hasattr(obj1, 'dimension')
    o2hasdim = hasattr(obj2, 'dimension')

    
    if (o1hasdim and o2hasdim) and (obj1.dim != obj2.dim).all(): # don't use None Type
        dim1 = obj1.dim
        dim2 = obj2.dim
        # Special treatment for "0":
        # if it is not a Quantity, it has "any dimension".
        # This allows expressions like 3*mV + 0 to pass (useful in cases where
        # zero is treated as the neutral element, e.g. in the Python sum
        # builtin) or comparisons like 3 * mV == 0 to return False instead of
        # failing # with a DimensionMismatchError. Note that 3*mV == 0*second
        # is not allowed, though.
        if (dim1.sum() == 0 and np.all(obj1 == 0) or
                (dim2.sum() == 0 and np.all(obj2 == 0))):
            return dim1, dim2

        # We do another check here, this should allow Brian1 units to pass as
        # having the same dimensions as a Brian2 unit
        if (dim1 == dim2).all():
            return dim1, dim2

        if error_message is None:
            error_message = 'Dimension mismatch'
        else:
            error_quantities = {name: _short_str(q)
                                for name, q in error_quantities.items()}
            error_message = error_message.format(**error_quantities)
        # If we are comparing an object to a specific unit, we don't want to
        # restate this unit (it is probably mentioned in the text already)
        if obj2 is None or isinstance(obj2, (Dimension, Unit)):
            raise DimensionMismatchError(error_message, dim1)
        else:
            raise DimensionMismatchError(error_message, dim1, dim2)
    else:
        if o1hasdim and o2hasdim:
            return obj1.dim, obj2.dim
        elif o2hasdim and obj1 != 0:
            raise DimensionMismatchError(error_message, obj2)
        elif o1hasdim and obj2 != 0:
            raise DimensionMismatchError(error_message, obj1)
        else:
            return None, None

def eval_dimension(units):
    dimension = np.zeros(7)
    try:
        for k, v in units.items():
            dimension += np.array(dims[k])*v
        return dimension
    except UnknownUnitError as e:
        raise UnknownUnitError(f'passed unit string {units} has unknown unit: {e}')

def eval_conversion_factor(units):
    factor = 1
    for k, v in units.items():
        factor *= conv[k]**v
    return factor


class Quantity(ndarray):
    def __new__(cls, arr, units, copy=False):

        subarr = np.array(arr, dtype=float, copy=copy).view(cls)

        if type(units) is str:
            units = unit_parse(units)

        subarr.units = units

        try:
            eval_dimension(units)
        except UnknownUnitError as e:
            raise UnknownUnitError(f'passed unit string {units} has unknown unit: {e}')

        return subarr

    @property
    def dimension(self):
        return eval_dimension(self.units)

    @property
    def dim(self):
        return self.dimension

    @property
    def conversion_factor(self):
        return eval_conversion_factor(self.units)

    def convert_to_SI(self):
        self *= self.conversion_factor
        d = self.dimension
        self.units = {'kg':d[0],
                      'm':d[1],
                      's':d[2],
                      'A':d[3],
                      'K':d[4],
                      'cd':d[5],
                      'mol':d[6]}
        return self

    def convert_to_unit(self, other_units):
        if type(other_units) is str:
            other_units = unit_parse(other_units) 
            
        try:
            assert (eval_dimension(other_units) == self.dimension).all()
        except AssertionError:
            raise DimensionMismatchError

        self *= eval_conversion_factor(self.units)/eval_conversion_factor(other_units)
        self.units = other_units
        return self

    #### ARITHMETIC #### (this is all copied from brian2)
    def _binary_operation(self, other, operation,
                          unit_operation=lambda a, b: a, fail_for_mismatch=False,
                          operator_str=None, inplace=False):

        if type(other) in [int, float]:
            other = Quantity([other], dict())

        if fail_for_mismatch:
            if inplace:
                message = ('Cannot calculate ... %s {value}, units do not '
                           'match') % operator_str
                _, other_dim = fail_for_dimension_mismatch(self, other,
                                                           message, value=other)
            else:
                message = ('Cannot calculate {value1} %s {value2}, units do not '
                           'match') % operator_str
                _, other_dim = fail_for_dimension_mismatch(self, other, message,
                                                           value1=self,
                                                           value2=other)

        if hasattr(other, 'units'): 
            other_units = other.units
        else:
            other_units = {}

        if inplace:
            if self.shape == ():
                self_value = Quantity(self, copy=True)
            else:
                self_value = self
            operation(self_value, other)
            self_value.units = unit_operation(self.units, other_units)
            return self_value
        else:
            newunits = unit_operation(self.units, other_units)
            self_arr = np.array(self, copy=False)
            other_arr = np.array(other, copy=False)
            result = operation(self_arr, other_arr)
            return Quantity(result, newunits)

    def __mul__(self, other):
        return self._binary_operation(other, operator.mul, d_add)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self._binary_operation(other, np.ndarray.__imul__, d_add,
                                      inplace=True)

    def __div__(self, other):
        return self._binary_operation(other, operator.truediv, d_sub)

    def __truediv__(self, other):
        return self.__div__(other)

    def __rdiv__(self, other):
        # division with swapped arguments
        rdiv = lambda a, b: operator.truediv(b, a)
        d_sub = lambda x, b: d_sub(b, a)
        return self._binary_operation(other, rdiv, d_sub)

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __idiv__(self, other):
        return self._binary_operation(other, np.ndarray.__itruediv__,
                                      d_sub, inplace=True)

    def __itruediv__(self, other):
        return self._binary_operation(other, np.ndarray.__itruediv__,
                                      d_sub, inplace=True)

    def __mod__(self, other):
        return self._binary_operation(other, operator.mod,
                                      fail_for_mismatch=True,operator_str=r'%')

    def __add__(self, other):
        return self._binary_operation(other, operator.add,
                                      fail_for_mismatch=True,
                                      operator_str='+')

    def __radd__(self, other):
        #not sure why rsub has complicated logic
        return self.__add__(other)

    def __iadd__(self, other):
        return self._binary_operation(other, np.ndarray.__iadd__,
                                      fail_for_mismatch=True,
                                      operator_str='+=',
                                      inplace=True)

    def __sub__(self, other):
        return self._binary_operation(other, operator.sub,
                                      fail_for_mismatch=True,
                                      operator_str='-')

    def __rsub__(self, other):
        # We allow operations with 0 even for dimension mismatches, e.g.
        # 0 - 3*mV is allowed. In this case, the 0 is not represented by a
        # Quantity object so we cannot simply call Quantity.__sub__
        if ((not isinstance(other, Quantity) or other.dim is DIMENSIONLESS) and
                np.all(other == 0)):
            return self.__neg__()
        else:
            return Quantity(other, copy=False, force_quantity=True).__sub__(self)

    def __isub__(self, other):
        return self._binary_operation(other, np.ndarray.__isub__,
                                      fail_for_mismatch=True,
                                      operator_str='-=',
                                      inplace=True)
    def __pow__(self, other):
        if isinstance(other, np.ndarray) or is_scalar_type(other):
            fail_for_dimension_mismatch(other,
                                        error_message='Cannot calculate '
                                                      '{base} ** {exponent}, '
                                                      'the exponent has to be '
                                                      'dimensionless',
                                        base=self, exponent=other)
            other = np.array(other, copy=False)
            return Quantity(np.array(self, copy=False)**other,
                            d_scale(self.units, other))
        else:
            return NotImplemented

    def __rpow__(self, other):
        if self.is_dimensionless:
            if isinstance(other, np.ndarray) or isinstance(other, np.ndarray):
                new_array = np.array(other, copy=False)**np.array(self,
                                                                  copy=False)
                return Quantity(new_array, DIMENSIONLESS)
            else:
                return NotImplemented
        else:
            raise DimensionMismatchError(('Cannot calculate '
                                          '{base} ** {exponent}, the '
                                          'exponent has to be '
                                          'dimensionless').format(base=_short_str(other),
                                                                  exponent=_short_str(self)),
                                         self.dim)
    def __ipow__(self, other):
        if isinstance(other, np.ndarray) or is_scalar_type(other):
            fail_for_dimension_mismatch(other,
                                        error_message='Cannot calculate '
                                                      '... **= {exponent}, '
                                                      'the exponent has to be '
                                                      'dimensionless',
                                        exponent=other)
            other = np.array(other, copy=False)
            super(Quantity, self).__ipow__(other)
            self.units = d_scale(self.units, other) 
            return self
        else:
            return NotImplemented

    def __neg__(self):
        return Quantity(-np.array(self, copy=False), self.units)

    def __pos__(self):
        return self

    def __abs__(self):
        return Quantity(abs(np.array(self, copy=False)), self.units)

    def __str__(self):
        fmted_val = ",".join(f"{x:.2f}" for x in self.tolist())
        fmted_uni = '*'.join(f'{k}^{v}' for k, v in self.units.items() if abs(v) > 0)
        return f'({fmted_val}) {fmted_uni}'
