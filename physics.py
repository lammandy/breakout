def intersects(obj_a, obj_b):
    xinside = obj_a.x + obj_a.w >= obj_b.x and obj_a.x <= obj_b.x + obj_b.w
    yinside = obj_a.y + obj_a.h >= obj_b.y and obj_a.y <= obj_b.y + obj_b.h
    return xinside and yinside


def collision(mover, static):
    if mover.speedx == 0 and mover.speedy == 0:
        return
    if not intersects(mover, static):
        return

    mover_btm = mover.y
    mover_top = mover.y + mover.h
    mover_lft = mover.x
    mover_rgt = mover.x + mover.w

    static_btm = static.y
    static_top = static.y + static.h
    static_lft = static.x
    static_rgt = static.x + static.w

    # btm lft collision
    if mover.speedx > 0 and mover.speedy > 0:
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
            return mover_x1, mover_y1, 'lft'
        else:
            return mover_x2, mover_y2, 'btm'

            
    # top rgt collision
    elif mover.speedx < 0 and mover.speedy < 0:
        x_delta = mover_lft - static_rgt # -
        y_delta = mover_btm - static_top # -
        # push out right
        mover_x1 = mover.x - x_delta
        mover_y1 = mover.y - x_delta / mover.speedx * mover.speedy # don't know why
        delta1 = mover_y1 - static_top

        #push out top
        mover_x2 = mover.x - y_delta / mover.speedy * mover.speedx
        mover_y2 = mover.y - y_delta
        delta2 = static_rgt - mover_x2
        
        if delta1 < delta2:
            return mover_x1, mover_y1, 'rgt'
        else:
            return mover_x2, mover_y2, 'top'

    # btm rgt collision
    elif mover.speedx < 0 and mover.speedy > 0:
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
            return mover_x1, mover_y1, 'rgt'
        else:
            return mover_x2, mover_y2, 'btm'


    # top lft collision
    elif mover.speedx > 0 and mover.speedy < 0:
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
            return mover_x1, mover_y1, 'lft'
        else:
            return mover_x2, mover_y2, 'top'
