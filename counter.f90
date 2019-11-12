program counter
    logical, dimension(5) :: C = .false.
    integer, dimension(5) :: ones = 1, zeros = 0, Cint

    Cint = merge(ones, zeros, C)
    print *, Cint
    do i=1, 32
        call increment_counter(C)
        Cint = merge(ones, zeros, C)
        print *, Cint
    end do

contains

function full_adder(a, b, carry_in)
    implicit none
    logical, intent(in) :: a, b, carry_in
    logical :: sum, carry_out, full_adder(2)
    sum = a .neqv. b .neqv. carry_in
    carry_out = a .and. b .or. carry_in .and. (a .neqv. b)
    full_adder = (/sum, carry_out /)
end function full_adder

subroutine increment_counter(C)
    implicit none
    logical, intent(inout) :: C(5)
    logical :: sumcarry(2)
    integer :: k
    sumcarry = full_adder(C(1), .true., .false.)
    C(1) = sumcarry(1)
    k = 2
    do while (sumcarry(2))
        sumcarry = full_adder(C(k), .false., sumcarry(2))
        C(k) = sumcarry(1)
        k = k+1
    end do
end subroutine increment_counter

end program counter
