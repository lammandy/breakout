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


def collision(mover, static, game_delta):
    if mover.speedx == 0 and mover.speedy == 0:
        return None
    tol = 0.001  #* max(abs(mover.speedx), abs(mover.speedy))

    want_x = mover.x + mover.speedx * game_delta
    want_y = mover.y + mover.speedy * game_delta

    if not will_intersect(mover, static, want_x, want_y):
        return None

    mover_btm = want_y
    mover_top = want_y + mover.h
    mover_lft = want_x
    mover_rgt = want_x + mover.w

    static_btm = static.y
    static_top = static.y + static.h
    static_lft = static.x
    static_rgt = static.x + static.w

    # coll time is the time between the last position before intersecting 
    # with the object(mover.x/y) and the intersecting position(want__x,y)
    # coll_time = (colly - mover.y) / (want_y - mover.y)
    # coll_time = (collx - mover.x) / (want_x - mover.x)

    if mover.speedy == 0:
        if mover.speedx > 0:
            # coll_time = ((static_lft - mover.w - tol) - mover.x) / (want_x - mover.x) * game_delta
            return static_lft - mover.w - tol, want_y, 'lft'  #, coll_time
        else:
            # coll_time = (static_rgt + tol - mover.x) / (want_x - mover.x) * game_delta
            return static_rgt + tol, want_y, 'rgt'  #, coll_time
    
    elif mover.speedx == 0:
        if mover.speedy > 0:
            # coll_time = ((static_btm - mover.h - tol) - want_y) / (want_y - want_y) * game_delta
            return want_x, static_btm - mover.h - tol, 'btm'  #, coll_time
        else:
            # coll_time = ((static_top + tol) - want_y) / (want_y - want_y) * game_delta
            return want_x, static_top + tol, 'top' #, coll_time

    # btm lft collision
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
            assert mover_top >= static_btm
            # coll_time = (mover_x1 - tol - want_x) / (want_x - want_x) * game_delta
            return mover_x1 - tol, mover_y1 - tol, 'lft'  #, coll_time
        else:
            assert mover_rgt >= static_lft
            # coll_time = (mover_y2 - tol - want_y) / (want_y - want_y) * game_delta
            return mover_x2 - tol, mover_y2 - tol, 'btm'  #, coll_time

            
    # top rgt collision
    elif mover.speedx <= 0 and mover.speedy <= 0:
        x_delta = mover_lft - static_rgt # -
        y_delta = mover_btm - static_top # -
        # push out right
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = mover_y1 - static_top # -?

        #push out top
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = static_rgt - mover_x2
        
        if delta1 > delta2: # TODO changed signs
            assert mover_lft <= static_rgt
            # print(f'delta1: {delta1}, delta2: {delta2}')
            #coll_time = (mover_x1 + tol - want_x) / (want_x - want_x) * game_delta
            return mover_x1 + tol, mover_y1 + tol, 'rgt' #, coll_time
        else:
            assert mover_btm <= static_top
            #coll_time = (mover_y2 + tol - want_y) / (want_y - want_y) * game_delta
            return mover_x2 + tol, mover_y2 + tol, 'top' #, coll_time

    # btm rgt collision
    elif mover.speedx <= 0 and mover.speedy >= 0:
        x_delta = mover_lft - static_rgt # negative
        y_delta = mover_top - static_btm
        # print(f'btm rgt collision: {x_delta, y_delta}')

        # push out right
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = static_btm - (mover_y1 + mover.h)

        # push out down
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = mover_x2 - static_rgt

        if delta1 < delta2:
            assert mover_lft <= static_rgt
            # print(f'delta1: {delta1}, delta2: {delta2}', 'btm rgt - rgt')
            #coll_time = (mover_x1 + tol - want_x) / (want_x - want_x) * game_delta
            return mover_x1 + tol, mover_y1 - tol, 'rgt'  #, coll_time
        else:
            assert mover_top >= static_btm
            # print(f'delta1: {delta1}, delta2: {delta2}', 'btm rgt - btm')
            #coll_time = (mover_y2 - tol - want_y) / (want_y - want_y) * game_delta
            return mover_x2 + tol, mover_y2 - tol, 'btm'  #, coll_time


    # top lft collision
    elif mover.speedx >= 0 and mover.speedy <= 0:
        x_delta = mover_rgt - static_lft
        y_delta = mover_btm - static_top #negative
            # print(f'top lft collision {x_delta, y_delta}')
        # push out left
        
        mover_x1 = want_x - x_delta
        mover_y1 = want_y - x_delta / mover.speedx * mover.speedy
        delta1 = mover_y1 - static_top # negative number?
        # push out up
        mover_x2 = want_x - y_delta / mover.speedy * mover.speedx
        mover_y2 = want_y - y_delta
        delta2 = static_lft - (mover_x2 + mover.w)

        if delta1 < delta2:
            assert mover_rgt >= static_lft, locals()
            #coll_time = (mover_x1 - tol - want_x) / (want_x - want_x) * game_delta
            return mover_x1 - tol, mover_y1 + tol, 'lft'   #, coll_time
        else:
            assert mover_btm <= static_top, locals()
            #coll_time = (mover_y2 + tol - want_y) / (want_y - want_y) * game_delta
            return mover_x2 - tol, mover_y2 + tol, 'top'  #, coll_time

# def still_collision(moving, static, list_obj, obj_types, game_delta):
#     # check if still is a collision based on time_moved. If time_moved = 0, then no collision


        
# def get_fraction(prev_pos, mover, static, game_delta, collisions):
#     prev_pos = want_x, want_y
#     want_x += mover.speedx * game_delta
#     want_y += mover.speedy * game_delta
#     collx, colly, collside = collisions
    
#     if collside == 'top' or collside == 'btm':
#         fraction_passed = (colly - prev_pos[1]) / (want_y - prev_pos[1])
#     if collside == 'lft' or collside == 'rgt':
#         fraction_passed = (collx - prev_pos[0]) / (want_x - prev_pos[0])
    
#     return fraction_passed, collx, colly, collside



# def get_fraction(prev_pos, mover, static, game_delta, collisions):
#     prev_pos = want_x, want_y
#     want_x += mover.speedx * game_delta
#     want_y += mover.speedy * game_delta
#     collx, colly, collside = collisions
    
#     if collside == 'top' or collside == 'btm':
#         fraction_passed = (colly - prev_pos[1]) / (want_y - prev_pos[1])
#     if collside == 'lft' or collside == 'rgt':
#         fraction_passed = (collx - prev_pos[0]) / (want_x - prev_pos[0])
    
#     return fraction_passed, collx, colly, collside