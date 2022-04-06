import nanoid


def generate_scenario_id():
    return str(
        nanoid.generate(
            alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
    )
