describe('content-script', () => {
  let port;

  beforeEach(() => {
    global.chrome = {
      runtime: {
        connect: jest.fn(),
      },
    };

    port = {
      onMessage: {
        addListener: jest.fn(),
      },
      onDisconnect: {
        addListener: jest.fn(),
      },
      postMessage: jest.fn(),
    };

    global.chrome.runtime.connect.mockReturnValue(port);

    window.postMessage = jest.fn();

    window.addEventListener = jest.fn();
    jest.resetModules();
    require('../content-script');
  });

  it('should connect to chrome runtime with the correct name', () => {
    expect(chrome.runtime.connect).toHaveBeenCalledWith({
      name: 'trezor-connect',
    });
  });

  it('should add a listener to port.onMessage', () => {
    expect(port.onMessage.addListener).toHaveBeenCalled();
  });

  it('should add a listener to port.onDisconnect', () => {
    expect(port.onDisconnect.addListener).toHaveBeenCalled();
  });

  it('should add a listener to window.postMessage', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'message',
      expect.any(Function)
    );
  });

  it('should set port is null when onDisconnect from port', () => {
    port.onDisconnect.addListener.mock.calls[0][0]();
  });

  it('should post message to window when receiving a message from port', () => {
    const message = { data: 'test message' };
    port.onMessage.addListener.mock.calls[0][0](message);
    expect(window.postMessage).toHaveBeenCalledWith(
      message,
      window.location.origin
    );
  });

  it('should post message to port when receiving a message from window', () => {
    const message = { data: 'test message' };
    const event = { source: window, data: message };
    window.addEventListener.mock.calls[0][1](event);
    expect(port.postMessage).toHaveBeenCalledWith({ data: message });
  });

  it('should not post message to port when receiving the event is invalid', () => {
    const event = {};
    window.addEventListener.mock.calls[0][1](event);
    expect(port.postMessage).not.toHaveBeenCalled();
  });
});
