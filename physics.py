import numpy as np

def intersects(lhs, rhs):
    return (
        ((rhs.x <= lhs.x <= rhs.x + rhs.w) or
        (rhs.x <= lhs.x + lhs.w <= rhs.x + rhs.w)) and
        ((rhs.y <= lhs.y <= rhs.y + rhs.h) or
        (rhs.y <= lhs.y + lhs.h <= rhs.y + rhs.h)))


def will_intersect(lhs, rhs, wantx, wanty):
    R1 = [rhs.x, rhs.y, rhs.x + rhs.w, rhs.y + rhs.h]
    R2 = [wantx, wanty, wantx + lhs.w, wanty + lhs.h]
    if (R1[0]>=R2[2]) or (R1[2]<=R2[0]) or (R1[3]<=R2[1]) or (R1[1]>=R2[3]):
        return False
    else:
        return True
    # return (
    #     ((rhs.x <= wantx <= rhs.x + rhs.w) or
    #     (rhs.x <= wantx + lhs.w <= rhs.x + rhs.w)) and
    #     ((rhs.y <= wanty <= rhs.y + rhs.h) or
    #     (rhs.y <= wanty + lhs.h <= rhs.y + rhs.h)))
def find_square_distance(collx, colly, mover_x, mover_y):
    sq_dist = (collx - mover_x) ** 2 + (colly - mover_y) ** 2
    return sq_dist

def find_collision(mover, static, duration):
    if mover.speedx == 0 and mover.speedy == 0:
        return

    want_x = mover.x + mover.speedx * duration
    want_y = mover.y + mover.speedy * duration

    if not will_intersect(mover, static, want_x, want_y):
        return
    # print(f'mover: {mover.updated}')
    # print(f'static: {static.updated}')    

    mover_btm = want_y
    mover_top = want_y + mover.h
    mover_lft = want_x
    mover_rgt = want_x + mover.w

    static_btm = static.y
    static_top = static.y + static.h
    static_lft = static.x
    static_rgt = static.x + static.w

    # find smaller square distance of mover.x/y to colliding side
    if mover.speedy == 0:
        if mover.speedx > 0:
            return static_lft - mover.w, want_y, 'lft'
            # return distance = 
        else:
            return static_rgt, want_y, 'rgt'

    elif mover.speedx == 0:
        if mover.speedy > 0:
            return want_x, static_btm - mover.h, 'btm'
        else:
            return want_x, static_top, 'top'

    elif mover.speedx >= 0 and mover.speedy >= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_top - static_btm

        # push out left
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        sq_dist_left = find_square_distance(mover_x1, mover_y1, mover.x, mover.y)

        # push out down
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        sq_dist_down = find_square_distance(mover_x2, mover_y2, mover.x, mover.y)

        if sq_dist_left < sq_dist_down:
            return mover_x1, mover_y1, 'lft'
        else:
            return mover_x2, mover_y2, 'btm'
            
    # top rgt collision
    elif mover.speedx <= 0 and mover.speedy <= 0:
        x_delta = mover_lft - static_rgt
        y_delta = mover_btm - static_top

        # push out right
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        sq_dist_right = find_square_distance(mover_x1, mover_y1, mover.x, mover.y)

        #push out top
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        sq_dist_top = find_square_distance(mover_x2, mover_y2, mover.x, mover.y)
        
        if sq_dist_right < sq_dist_top: # TODO changed sign
            return mover_x1, mover_y1, 'rgt'
        else:
            return mover_x2, mover_y2, 'top'

    # btm rgt collision
    elif mover.speedx <= 0 and mover.speedy >= 0:
        x_delta = mover_lft - static_rgt
        y_delta = mover_top - static_btm

        # push out right
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        sq_dist_right = find_square_distance(mover_x1, mover_y1, mover.x, mover.y)

        # push out down
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        sq_dist_down = find_square_distance(mover_x2, mover_y2, mover.x, mover.y)

        if sq_dist_right < sq_dist_down:
            return mover_x1, mover_y1, 'rgt'
        else:
            return mover_x2, mover_y2, 'btm'

    # top lft collision
    elif mover.speedx >= 0 and mover.speedy <= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_btm - static_top

        # push out left
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        sq_dist_left = find_square_distance(mover_x1, mover_y1, mover.x, mover.y)

        # push out up
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        sq_dist_down = find_square_distance(mover_x2, mover_y2, mover.x, mover.y)

        if sq_dist_left < sq_dist_down:
            return mover_x1, mover_y1, 'lft'
        else:
            return mover_x2, mover_y2, 'top'
    

# obj_types = Wall, Brick, Paddle, Death
def move_until_collision(mover, objects, obj_types, duration, tol=0.0001):
    prev_x = mover.x
    prev_y = mover.y
    want_x = mover.x + mover.speedx * duration
    want_y = mover.y + mover.speedy * duration

    frac_moved = None
    dist = None
    collision = None
    for obj in objects:
        if not isinstance(obj, obj_types):
            continue
        current = find_collision(mover, obj, duration)

        # prev pos -> want
        # new_dist = np.sqrt((want_x + mover.w/2 - prev_x + mover.w/2) ** 2 + (want_y + mover.h/2 - prev_y + mover.h/2) ** 2)
        # prev pos -> static
        # new_dist = np.sqrt((obj.x + obj.w/2 - prev_x + mover.w/2) ** 2 + (obj.y + obj.h/2 - prev_y + mover.h/2) ** 2) 

        if not current:
            continue
        coll_x, coll_y, coll_side = current
        # prev pos -> coll
        new_dist = np.sqrt((coll_x - prev_x) ** 2 + (coll_y - prev_y) ** 2)
        # calcumalkate the fraction

        # if coll_side == "lft" or coll_side == "rgt":
        #     new_frac_moved = (coll_x - prev_x) / (want_x - prev_x)
        # if coll_side == "top" or coll_side == "btm":
        #     new_frac_moved = (coll_y - prev_y) / (want_y - prev_y)
        # if not frac_moved or frac_moved > new_frac_moved:
        #     frac_moved = new_frac_moved
        #     collision = coll_x, coll_y, coll_side, obj
            
        if not dist or dist > new_dist:
            dist = new_dist
            collision = coll_x, coll_y, coll_side, obj

    # prev pos -> coll, prev pos -> want, prev pos -> static : find the one that is closests to..??
    # how many things am i colliding with - use a counter

    if collision:
        coll_x, coll_y, coll_side, obj = collision
        #calculmalate the fraction
        total = np.sqrt((want_x - prev_x) ** 2 + (want_y - prev_y) ** 2)
        frac_moved = dist / total
        mover.x = coll_x - tol * mover.speedx
        mover.y = coll_y - tol * mover.speedy
        obj.on_collision(mover, coll_side)
        if coll_side == 'lft' or coll_side == 'rgt':
            mover.speedx *= -1
        if coll_side == 'top' or coll_side == 'btm':
            mover.speedy *= -1
        return duration * (1 - frac_moved), obj, coll_side
    else:
        mover.x = want_x
        mover.y = want_y

        return 0, None, None


# for paddle collision, return a boolean in main in the game loop to check if update has been performed on an object
# if not, calculate the position of where the collided object would be had it been updated