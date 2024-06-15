import threading

class Promise:
    def __init__(self):
        # Initialize the promise with default values
        self.resolved = False  # Flag to indicate if the promise is resolved
        self.rejected = False  # Flag to indicate if the promise is rejected
        self.value = None  # Value to be returned when the promise is resolved
        self.error = None  # Error to be returned when the promise is rejected
        self.then_callback = None  # Callback to be called when the promise is resolved
        self.catch_callback = None  # Callback to be called when the promise is rejected
        self.lock = threading.Lock()  # Lock to ensure thread-safe access to the promise's state

    def then(self, callback):
        # Register a callback to be called when the promise is resolved
        with self.lock:
            # Acquire the lock to ensure thread-safe access
            if self.resolved:
                # If the promise is already resolved, call the callback immediately
                callback(self.value)
            else:
                # If the promise is not resolved, store the callback to be called later
                self.then_callback = callback
        return self

    def catch(self, callback):
        # Register a callback to be called when the promise is rejected
        with self.lock:
            # Acquire the lock to ensure thread-safe access
            if self.rejected:
                # If the promise is already rejected, call the callback immediately
                callback(self.error)
            else:
                # If the promise is not rejected, store the callback to be called later
                self.catch_callback = callback
        return self

    def resolve(self, value):
        # Resolve the promise with a given value
        threading.Thread(target=self.do_resolve, args=(value,)).start()

    def do_resolve(self, value):
        try:
            # Try to resolve the promise with the given value
            # Call the value function to get the actual value
            v = value()
            # Set the result of the promise to the value
            self._set_result(v)
        except Exception as e:
            # If an exception occurs, reject the promise with the error
            self._set_error(e)

    def reject(self, error):
        # Reject the promise with a given error
        self._set_error(error)

    def _set_result(self, value):
        # Set the result of the promise to a given value
        with self.lock:
            # Acquire the lock to ensure thread-safe access
            if not self.resolved and not self.rejected:
                # If the promise is not already resolved or rejected
                self.value = value
                self.resolved = True
                # Set the promise to the resolved state
                if self.then_callback:
                    # If a then callback is registered, call it with the value
                    self.then_callback(value)

    def _set_error(self, error):
        # Set the error of the promise to a given error
        with self.lock:
            # Acquire the lock to ensure thread-safe access
            if not self.rejected and not self.resolved:
                # If the promise is not already rejected or resolved
                self.rejected = True
                self.error = error
                # Set the promise to the rejected state
                if self.catch_callback:
                    # If a catch callback is registered, call it with the error
                    self.catch_callback(error)