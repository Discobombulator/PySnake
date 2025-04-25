def check_end_game(head_position, player_id, snakes, obstacles, field_height,
                   field_width):
    # Проверка 1: Столкновение со стенами поля
    row, col = head_position
    if row < 0 or row >= field_height or col < 0 or col >= field_width:
        return True

    # Проверка 2: Столкновение с препятствием
    if head_position in obstacles:
        return True

    # Проверка 3: Столкновение с другими змеями
    # Перебираем всех змей и проверяем, не пересекается ли голова с телами других змей
    for snake_id, snake_data in snakes.items():
        snake_body = snake_data['body']

        # Если это другая змея - проверяем столкновение с любой частью её тела
        if snake_id != player_id and head_position in snake_body:
            return True

        # Если это наша змея - проверяем столкновение только с её телом (кроме головы)
        elif snake_id == player_id and head_position in snake_body[1:]:
            return True

    # Если ни одно из условий смерти не выполнено, змея остается жива
    return False