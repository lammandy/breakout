from re import X


def intersects(lhs, rhs):
    return (
        ((rhs.x <= lhs.x <= rhs.x + rhs.w) or
        (rhs.x <= lhs.x + lhs.w <= rhs.x + rhs.w)) and
        ((rhs.y <= lhs.y <= rhs.y + rhs.h) or
        (rhs.y <= lhs.y + lhs.h <= rhs.y + rhs.h)))


def will_intersect(lhs, rhs, wantx, wanty):
    return (
        ((rhs.x <= wantx <= rhs.x + rhs.w) or
        (rhs.x <= wantx + lhs.w <= rhs.x + rhs.w)) and
        ((rhs.y <= wanty <= rhs.y + rhs.h) or
        (rhs.y <= wanty + lhs.h <= rhs.y + rhs.h)))


def find_collision(mover, static, duration, tol=0.001):
    if mover.speedx == 0 and mover.speedy == 0:
        return

    want_x = mover.x + mover.speedx * duration
    want_y = mover.y + mover.speedy * duration

    if not will_intersect(mover, static, want_x, want_y):
        return

    mover_btm = want_y
    mover_top = want_y + mover.h
    mover_lft = want_x
    mover_rgt = want_x + mover.w

    static_btm = static.y
    static_top = static.y + static.h
    static_lft = static.x
    static_rgt = static.x + static.w

    if mover.speedy == 0:
        if mover.speedx > 0:
            return static_lft - mover.w - tol, want_y, 'lft'
        else:
            return static_rgt + tol, want_y, 'rgt'

    elif mover.speedx == 0:
        if mover.speedy > 0:
            return want_x, static_btm - mover.h - tol, 'btm'
        else:
            return want_x, static_top + tol, 'top'

    elif mover.speedx >= 0 and mover.speedy >= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_top - static_btm

        # push out left
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = static_btm - (mover_y1 + mover.h)

        # push out down
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = static_lft - (mover_x2 + mover.w)

        if delta1 < delta2:
            return mover_x1 - tol, mover_y1 - tol, 'lft'
        else:
            return mover_x2 - tol, mover_y2 - tol, 'btm'
            
    # top rgt collision
    elif mover.speedx <= 0 and mover.speedy <= 0:
        x_delta = mover_lft - static_rgt
        y_delta = mover_btm - static_top

        # push out right
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = mover_y1 - static_top

        #push out top
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = static_rgt - mover_x2
        
        if delta1 > delta2:
            return mover_x1 + tol, mover_y1 + tol, 'rgt'
        else:
            return mover_x2 + tol, mover_y2 + tol, 'top'

    # btm rgt collision
    elif mover.speedx <= 0 and mover.speedy >= 0:
        x_delta = mover_lft - static_rgt
        y_delta = mover_top - static_btm

        # push out right
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = static_btm - (mover_y1 + mover.h)

        # push out down
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = mover_x2 - static_rgt

        if delta1 < delta2:
            return mover_x1 + tol, mover_y1 - tol, 'rgt'
        else:
            return mover_x2 + tol, mover_y2 - tol, 'btm'

    # top lft collision
    elif mover.speedx >= 0 and mover.speedy <= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_btm - static_top

        # push out left
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = mover_y1 - static_top

        # push out up
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = static_lft - (mover_x2 + mover.w)

        if delta1 < delta2:
            return mover_x1 - tol, mover_y1 + tol, 'lft'
        else:
            return mover_x2 - tol, mover_y2 + tol, 'top'


# obj_types = Wall, Brick, Paddle, Death
def move_until_collision(mover, objects, obj_types, duration):
    prev_x = mover.x
    prev_y = mover.y
    want_x = mover.x + mover.speedx * duration
    want_y = mover.y + mover.speedy * duration

    frac_moved = None
    collision = None
    for obj in objects:
        if not isinstance(obj, obj_types):
            continue
        current = find_collision(mover, obj, duration)

        if not current:
            continue
        coll_x, coll_y, coll_side = current
        if coll_side == "lft" or coll_side == "rgt":
            new_frac_moved = (coll_x - prev_x) / (want_x - prev_x)
        if coll_side == "top" or coll_side == "btm":
            new_frac_moved = (coll_y - prev_y) / (want_y - prev_y)
        if not frac_moved or frac_moved > new_frac_moved:
            frac_moved = new_frac_moved
            collision = coll_x, coll_y, coll_side, obj
    

    
    if collision:
        coll_x, coll_y, coll_side, obj = collision
        mover.x = coll_x
        mover.y = coll_y
        obj.on_collision(mover, coll_side)
        if coll_side == 'lft' or coll_side == 'rgt':
            mover.speedx *= -1
        if coll_side == 'top' or coll_side == 'btm':
            mover.speedy *= -1
        return duration * (1 - frac_moved)
    else:
        mover.x = want_x
        mover.y = want_y

        return 0


# for paddle collision, return a boolean in main in the game loop to check if update has been performed on an object
# if not, calculate the position of where the collided object would be had it been updated