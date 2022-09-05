def intersects(lhs, rhs):
    xinside = rhs.x <= lhs.x + lhs.w and lhs.x <= rhs.x + rhs.w
    yinside = rhs.y <= lhs.y + lhs.h and lhs.y <= rhs.y + rhs.h
    return xinside and yinside
    # return (
    #     ((rhs.x <= lhs.x <= rhs.x + rhs.w) or
    #     (rhs.x <= lhs.x + lhs.w <= rhs.x + rhs.w)) and
    #     ((rhs.y <= lhs.y <= rhs.y + rhs.h) or
    #     (rhs.y <= lhs.y + lhs.h <= rhs.y + rhs.h)))


def collision(mover, static):
    if mover.speedx == 0 and mover.speedy == 0:
        return
    if not intersects(mover, static):
        return
    tol = 0.001  #* max(abs(mover.speedx), abs(mover.speedy))

    mover_btm = mover.y
    mover_top = mover.y + mover.h
    mover_lft = mover.x
    mover_rgt = mover.x + mover.w

    static_btm = static.y
    static_top = static.y + static.h
    static_lft = static.x
    static_rgt = static.x + static.w

    if mover.speedy == 0:
        if mover.speedx > 0:
            return static_lft - mover.w - tol, mover.y, 'lft'
        else:
            return static_rgt + tol, mover.y, 'rgt'
    
    elif mover.speedx == 0:
        if mover.speedy > 0:
            return mover.x, static_btm - mover.h - tol, 'btm'
        else:
            return mover.x, static_top + tol, 'top'

    # btm lft collision
    elif mover.speedx >= 0 and mover.speedy >= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_top - static_btm

        # push out left
        mover_x1 = mover.x - x_delta
        mover_y1 = mover.y - x_delta / mover.speedx * mover.speedy
        delta1 = static_btm - (mover_y1 + mover.h)

        # push out down
        mover_x2 = mover.x - y_delta / mover.speedy * mover.speedx
        mover_y2 = mover.y - y_delta
        delta2 = static_lft - (mover_x2 + mover.w)
 
        if delta1 < delta2:
            assert mover_top >= static_btm
            return mover_x1 - tol, mover_y1 - tol, 'lft'
        else:
            assert mover_rgt >= static_lft
            return mover_x2 - tol, mover_y2 - tol, 'btm'

            
    # top rgt collision
    elif mover.speedx <= 0 and mover.speedy <= 0:
        x_delta = mover_lft - static_rgt # -
        y_delta = mover_btm - static_top # -
        # push out right
        mover_x1 = mover.x - x_delta
        mover_y1 = mover.y - x_delta / mover.speedx * mover.speedy # don't know why
        delta1 = mover_y1 - static_top # -?

        #push out top
        mover_x2 = mover.x - y_delta / mover.speedy * mover.speedx
        mover_y2 = mover.y - y_delta
        delta2 = static_rgt - mover_x2
        
        if delta1 > delta2: # TODO changed signs
            assert mover_lft <= static_rgt
            print(f'delta1: {delta1}, delta2: {delta2}')
            return mover_x1 + tol, mover_y1 + tol, 'rgt'
        else:
            assert mover_btm <= static_top
            return mover_x2 + tol, mover_y2 + tol, 'top'

    # btm rgt collision
    elif mover.speedx <= 0 and mover.speedy >= 0:
        x_delta = mover_lft - static_rgt # negative
        y_delta = mover_top - static_btm
        # print(f'btm rgt collision: {x_delta, y_delta}')

        # push out right
        mover_x1 = mover.x - x_delta
        mover_y1 = mover.y - x_delta / mover.speedx * mover.speedy
        delta1 = static_btm - (mover_y1 + mover.h)

        # push out down
        mover_x2 = mover.x - y_delta / mover.speedy * mover.speedx
        mover_y2 = mover.y - y_delta
        delta2 = mover_x2 - static_rgt

        if delta1 < delta2:
            assert mover_lft <= static_rgt
            print(f'delta1: {delta1}, delta2: {delta2}', 'btm rgt - rgt')
            return mover_x1 + tol, mover_y1 - tol, 'rgt'
        else:
            assert mover_top >= static_btm
            print(f'delta1: {delta1}, delta2: {delta2}', 'btm rgt - btm')

            return mover_x2 + tol, mover_y2 - tol, 'btm'


    # top lft collision
    elif mover.speedx >= 0 and mover.speedy <= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_btm - static_top #negative
            # print(f'top lft collision {x_delta, y_delta}')
        # push out left
        
        mover_x1 = mover.x - x_delta
        mover_y1 = mover.y - x_delta / mover.speedx * mover.speedy
        delta1 = mover_y1 - static_top # negative number?
        # push out up
        mover_x2 = mover.x - y_delta / mover.speedy * mover.speedx
        mover_y2 = mover.y - y_delta
        delta2 = static_lft - (mover_x2 + mover.w)

        if delta1 < delta2:
            assert mover_rgt >= static_lft, locals()
            return mover_x1 - tol, mover_y1 + tol, 'lft'
        else:
            assert mover_btm <= static_top, locals()
            return mover_x2 - tol, mover_y2 + tol, 'top'
