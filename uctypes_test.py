import uctypes

ACCEL_CONFIG = {
    'x_self_test'   : uctypes.BFUINT8 | 0 | 7 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
    'y_self_test'   : uctypes.BFUINT8 | 0 | 6 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
    'z_self_test'   : uctypes.BFUINT8 | 0 | 5 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
    'range'         : uctypes.BFUINT8 | 0 | 3 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
}

buf = bytearray(1)
buf[0] = 0xa8
print('buf[0] =', hex(buf[0]))

accel_config = uctypes.struct(ACCEL_CONFIG, uctypes.addressof(buf))
print('x_self_test =', accel_config.x_self_test)
print('y_self_test =', accel_config.y_self_test)
print('z_self_test =', accel_config.z_self_test)
print('range =', accel_config.range)

accel_config.y_self_test = 1
print('buf[0] =', hex(buf[0]))

