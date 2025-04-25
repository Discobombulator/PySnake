def check_end_game_mult(new_head, player_id, snakes, obstacles,
                        field_height, field_width):
    # Проверка столкновения со стеной
    if (new_head[0] < 0 or new_head[0] >= field_height or
            new_head[1] < 0 or new_head[1] >= field_width):
        return True

    # Проверка столкновения с препятствием
    if new_head in obstacles:
        return True

    # Проверка столкновения с телом своей змеи
    if player_id in snakes:
        snake = snakes[player_id]
        # Проверяем со 2-й позиции, т.к. голова сейчас в new_head
        if new_head in snake['body'][1:]:
            return True

    # Проверка столкновения с другими змеями
    for pid, snake in snakes.items():
        if pid != player_id:  # Не проверяем столкновение с самим собой
            if new_head in snake['body']:
                return True

    return False
