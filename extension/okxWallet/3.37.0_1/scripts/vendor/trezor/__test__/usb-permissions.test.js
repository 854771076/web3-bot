describe('usb-permissions', () => {
  beforeEach(() => {
    global.chrome = {
      runtime: {
        id: 'extension',
      },
      tabs: {
        query: jest.fn(),
        update: jest.fn(),
        remove: jest.fn(),
      },
    };

    window.removeEventListener = jest.fn();
    window.addEventListener = jest.fn();

    jest.resetModules();
    require('../usb-permissions');
  });

  it('should add a listener to a beforeunload event if event and tabs are not empty', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    chrome.tabs.query.mockImplementation((_, callback) =>
      callback([{ index: 1, id: 1 }])
    );
    window.addEventListener.mock.calls[1][1]({});
    expect(window.removeEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        url: '*://connect.trezor.io/*/popup.html',
      },
      expect.any(Function)
    );
    expect(chrome.tabs.update).toHaveBeenCalledWith(1, { active: true });
  });

  it('should add a listener to a beforeunload event if event is exist, but tabs is empty', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    chrome.tabs.query.mockImplementation((_, callback) => callback([]));
    window.addEventListener.mock.calls[1][1]({});
    expect(window.removeEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        url: '*://connect.trezor.io/*/popup.html',
      },
      expect.any(Function)
    );
    expect(chrome.tabs.update).not.toHaveBeenCalled();
  });

  it('should add a listener to a beforeunload event if event is not exist and tabs is not empty', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    chrome.tabs.query
      .mockImplementationOnce((_, callback) => callback([{ index: 1, id: 1 }]))
      .mockImplementationOnce((_, callback) => callback([{ index: 0, id: 0 }]));
    window.addEventListener.mock.calls[1][1]();
    expect(window.removeEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        currentWindow: true,
        active: true,
      },
      expect.any(Function)
    );
    expect(chrome.tabs.remove).toHaveBeenCalledWith(1);
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        index: 0,
      },
      expect.any(Function)
    );
    expect(chrome.tabs.update).toHaveBeenCalledWith(0, { active: true });
  });

  it('should add a listener to a beforeunload event if event is not exist and index tab is empty', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    chrome.tabs.query
      .mockImplementationOnce((_, callback) => callback([{ index: 1, id: 1 }]))
      .mockImplementationOnce((_, callback) => callback([]));
    window.addEventListener.mock.calls[1][1]();
    expect(window.removeEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        currentWindow: true,
        active: true,
      },
      expect.any(Function)
    );
    expect(chrome.tabs.remove).toHaveBeenCalledWith(1);
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        index: 0,
      },
      expect.any(Function)
    );
    expect(chrome.tabs.update).not.toHaveBeenCalled();
  });

  it('should add a listener to a beforeunload event if event is not exist and currentWindow is empty', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    chrome.tabs.query.mockImplementationOnce((_, callback) => callback([]));
    window.addEventListener.mock.calls[1][1]();
    expect(window.removeEventListener).toHaveBeenCalledWith(
      'beforeunload',
      expect.any(Function)
    );
    expect(chrome.tabs.query).toHaveBeenCalledWith(
      {
        currentWindow: true,
        active: true,
      },
      expect.any(Function)
    );
  });

  it('should add a listener to a message event if event.data is usb-permissions-init', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'message',
      expect.any(Function)
    );
    const iframe = {
      contentWindow: { postMessage: jest.fn() },
    };
    document.getElementById = jest.fn().mockReturnValue(iframe);
    window.addEventListener.mock.calls[0][1]({ data: 'usb-permissions-init' });
    expect(document.getElementById).toHaveBeenCalledWith(
      'trezor-usb-permissions'
    );
    expect(iframe.contentWindow.postMessage).toHaveBeenCalledWith(
      {
        type: 'usb-permissions-init',
        extension: chrome.runtime.id,
      },
      '*'
    );
  });

  it('should add a listener to a message event if event.data is usb-permissions-close', () => {
    expect(window.addEventListener).toHaveBeenCalledWith(
      'message',
      expect.any(Function)
    );
    chrome.tabs.query.mockImplementationOnce((_, callback) => callback([]));
    window.addEventListener.mock.calls[0][1]({ data: 'usb-permissions-close' });
    window.addEventListener.mock.calls[0][1]({ data: 'nothing' });
  });
});
