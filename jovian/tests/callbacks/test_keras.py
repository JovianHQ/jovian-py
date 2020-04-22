from unittest import mock
from unittest.mock import ANY
import pytest
import sys
import numpy as np

try:
    from keras.layers import Dense, Dropout
    from keras.models import Sequential

    from jovian.callbacks.keras import JovianKerasCallback
    from jovian.callbacks.keras import Encoder
except:
    print('Tensorflow needs Python 3.7 or lower')
    pass


@pytest.mark.skipif(sys.version_info > (3, 7), reason="requires python3.7 or lower")
@pytest.mark.parametrize(
    "data, encoded_type",
    [
        (np.int64(42), int),
        (np.float64(42.24), float),
        (np.ndarray([1, 2, 3]), list),
    ]
)
def test_encoder(data, encoded_type):
    enc = Encoder()
    assert isinstance(enc.default(data), encoded_type)


@pytest.fixture
def model():
    model = Sequential()
    model.add(Dense(64, input_dim=20, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    return model


@pytest.mark.skipif(sys.version_info > (3, 7), reason="requires python3.7 or lower")
@mock.patch("jovian.callbacks.keras.notify")
@mock.patch("jovian.callbacks.keras.log_hyperparams")
@mock.patch("jovian.callbacks.keras.log_metrics")
def test_keras(mock_log_metrics, mock_log_hyperparams, mock_notify, model):
    # Generate dummy data
    x_train = np.random.random((1000, 20))
    y_train = np.random.randint(2, size=(1000, 1))
    x_test = np.random.random((100, 20))
    y_test = np.random.randint(2, size=(100, 1))

    # every_epoch = False
    jvn_cb = JovianKerasCallback(arch_name='custom1', every_epoch=False, notify=True)
    model.fit(x_train, y_train,
              epochs=1,
              batch_size=128,
              callbacks=[jvn_cb])

    mock_log_hyperparams.assert_called_with({
        'epochs': 1,
        'batch_size': 128,
        'loss_func': 'binary_crossentropy',
        'opt': 'RMSprop',
        'wt_decay': 0.0,
        'lr': '0.001',
        'arch': 'custom1'
    }, verbose=False)

    mock_log_metrics.assert_called_with({
        'loss': ANY,
        'accuracy': ANY
    }, verbose=False)

    mock_notify.assert_called_with(ANY, safe=True, verbose=False)

    # every_epoch = True
    jvn_cb = JovianKerasCallback(arch_name='custom1', every_epoch=True)
    model.fit(x_train, y_train,
              epochs=1,
              batch_size=128,
              callbacks=[jvn_cb])

    mock_log_hyperparams.assert_called_with({
        'epochs': 1,
        'batch_size': 128,
        'loss_func': 'binary_crossentropy',
        'opt': 'RMSprop',
        'wt_decay': 0.0,
        'lr': '0.001',
        'arch': 'custom1'
    }, verbose=False)

    mock_log_metrics.assert_called_with({
        'epoch': 0,
        'loss': ANY,
        'accuracy': ANY
    }, verbose=False)
