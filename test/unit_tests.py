from pymunk import Vec2d

from game.internal_ship.ship_panels import RotationDrive
import pytest

from game.unit_transformation import (
    PygamePymunkImplementationUnitsTransformer as Transformer,
)
import math


@pytest.mark.parametrize(
    ["current_angle", "target_angle", "expected_result"],
    (
        (0, 90, 90),
        (90, 0, -90),
        (0, 0, 0),
        (270, 0, 90),
        (0, 270, -90),
        (45, 270, -135),
        (270, 45, 135),
    ),
)
def test_rotation_value(current_angle, target_angle, expected_result):
    module = RotationDrive(tick_rotation=5)
    rotation = module._get_rotation_value(current_angle, target_angle)
    assert rotation == expected_result


class TestPygamePymunkImplementationUnitsTransformer:
    @pytest.mark.parametrize(
        ("input_value", "expected_result"),
        (
            ((0, 0), (0, 0)),
            ((1, 0), (1, 0)),
            ((0, 1), (0, -1)),
            ((1, 1), (1, -1)),
            ((-1, 0), (-1, 0)),
            ((-1, 1), (-1, -1)),
            ((-1, -1), (-1, 1)),
            ((1, -1), (1, 1)),
            ((0, -1), (0, 1)),
        ),
    )
    def test_to_impl_position(self, input_value, expected_result):
        result = Transformer.to_impl_position(Vec2d(input_value[0], input_value[1]))
        assert result == Vec2d(expected_result[0], expected_result[1])

    @pytest.mark.parametrize(
        ("expected_result", "input_value"),
        (
            ((0, 0), (0, 0)),
            ((1, 0), (1, 0)),
            ((0, 1), (0, -1)),
            ((1, 1), (1, -1)),
            ((-1, 0), (-1, 0)),
            ((-1, 1), (-1, -1)),
            ((-1, -1), (-1, 1)),
            ((1, -1), (1, 1)),
            ((0, -1), (0, 1)),
        ),
    )
    def test_from_impl_position(self, expected_result, input_value):
        result = Transformer.from_impl_position(Vec2d(input_value[0], input_value[1]))
        assert result == Vec2d(expected_result[0], expected_result[1])

    @pytest.mark.parametrize(
        ("input_value", "expected_result"),
        (
            (0, math.radians(270)),
            (90, math.radians(0)),
            (180, math.radians(90)),
            (270, math.radians(180)),
            (360, math.radians(270)),
        ),
    )
    def test_to_impl_angle(self, input_value, expected_result):
        result = Transformer.to_impl_angle(input_value)
        assert result == expected_result

    @pytest.mark.parametrize(
        ("expected_result", "input_value"),
        (
            (0, math.radians(270)),
            (90, math.radians(0)),
            (90, math.radians(360)),
            (180, math.radians(90)),
            (270, math.radians(180)),
        ),
    )
    def test_from_impl_angle(self, expected_result, input_value):
        result = Transformer.from_impl_angle(input_value)
        assert result == expected_result
