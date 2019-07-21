# http://docs.jinkan.org/docs/flask/

## 最小系统
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

## app.run()
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        """Runs the application on a local development server.

        Do not use ``run()`` in a production setting. It is not intended to
        meet security and performance requirements for a production server.
        Instead, see :ref:`deployment` for WSGI server recommendations.

        If the :attr:`debug` flag is set the server will automatically reload
        for code changes and show a debugger in case an exception happened.

        If you want to run the application in debug mode, but disable the
        code execution on the interactive debugger, you can pass
        ``use_evalex=False`` as parameter.  This will keep the debugger's
        traceback screen active, but disable code execution.

        It is not recommended to use this function for development with
        automatic reloading as this is badly supported.  Instead you should
        be using the :command:`flask` command line script's ``run`` support.

        .. admonition:: Keep in Mind

           Flask will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to ``True`` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.

        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
            have the server available externally as well. Defaults to
            ``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
            if present.
        :param port: the port of the webserver. Defaults to ``5000`` or the
            port defined in the ``SERVER_NAME`` config variable if present.
        :param debug: if given, enable or disable debug mode. See
            :attr:`debug`.
        :param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
            files to set environment variables. Will also change the working
            directory to the directory containing the first file found.
        :param options: the options to be forwarded to the underlying Werkzeug
            server. See :func:`werkzeug.serving.run_simple` for more
            information.

        .. versionchanged:: 1.0
            If installed, python-dotenv will be used to load environment
            variables from :file:`.env` and :file:`.flaskenv` files.

            If set, the :envvar:`FLASK_ENV` and :envvar:`FLASK_DEBUG`
            environment variables will override :attr:`env` and
            :attr:`debug`.

            Threaded mode is enabled by default.

        .. versionchanged:: 0.10
            The default port is now picked from the ``SERVER_NAME``
            variable.
        """
        # Change this into a no-op if the server is invoked from the
        # command line. Have a look at cli.py for more information.
        if os.environ.get("FLASK_RUN_FROM_CLI") == "true":
            from .debughelpers import explain_ignored_app_run

            explain_ignored_app_run()
            return

        if get_load_dotenv(load_dotenv):
            cli.load_dotenv()

            # if set, let env vars override previous values
            if "FLASK_ENV" in os.environ:
                self.env = get_env()
                self.debug = get_debug_flag()
            elif "FLASK_DEBUG" in os.environ:
                self.debug = get_debug_flag()

        # debug passed to method overrides all other sources
        if debug is not None:
            self.debug = bool(debug)

        _host = "127.0.0.1"
        _port = 5000
        server_name = self.config.get("SERVER_NAME")
        sn_host, sn_port = None, None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        host = host or sn_host or _host
        # pick the first value that's not None (0 is allowed)
        port = int(next((p for p in (port, sn_port) if p is not None), _port))

        options.setdefault("use_reloader", self.debug)
        options.setdefault("use_debugger", self.debug)
        options.setdefault("threaded", True)

        cli.show_server_banner(self.env, self.debug, self.name, False)

        from werkzeug.serving import run_simple

        try:
            run_simple(host, port, self, **options)
        finally:
            # reset the first request information if the development server
            # reset normally.  This makes it possible to restart the server
            # without reloader and that stuff from an interactive shell.
            self._got_first_request = False


 ## run_simple
 from werkzeug.serving import run_simple

        try:
            run_simple(host, port, self, **options)
        finally:
            # reset the first request information if the development server
            # reset normally.  This makes it possible to restart the server
            # without reloader and that stuff from an interactive shell.
            self._got_first_request = False

  ## run_simple func

def run_simple(hostname, port, application, use_reloader=False,
               use_debugger=False, use_evalex=True,
               extra_files=None, reloader_interval=1,
               reloader_type='auto', threaded=False,
               processes=1, request_handler=None, static_files=None,
               passthrough_errors=False, ssl_context=None):
    """Start a WSGI application. Optional features include a reloader,
    multithreading and fork support.

    This function has a command-line interface too::

        python -m werkzeug.serving --help

    .. versionadded:: 0.5
       `static_files` was added to simplify serving of static files as well
       as `passthrough_errors`.

    .. versionadded:: 0.6
       support for SSL was added.

    .. versionadded:: 0.8
       Added support for automatically loading a SSL context from certificate
       file and private key.

    .. versionadded:: 0.9
       Added command-line interface.

    .. versionadded:: 0.10
       Improved the reloader and added support for changing the backend
       through the `reloader_type` parameter.  See :ref:`reloader`
       for more information.

    :param hostname: The host for the application.  eg: ``'localhost'``
    :param port: The port for the server.  eg: ``8080``
    :param application: the WSGI application to execute
    :param use_reloader: should the server automatically restart the python
                         process if modules were changed?
    :param use_debugger: should the werkzeug debugging system be used?
    :param use_evalex: should the exception evaluation feature be enabled?
    :param extra_files: a list of files the reloader should watch
                        additionally to the modules.  For example configuration
                        files.
    :param reloader_interval: the interval for the reloader in seconds.
    :param reloader_type: the type of reloader to use.  The default is
                          auto detection.  Valid values are ``'stat'`` and
                          ``'watchdog'``. See :ref:`reloader` for more
                          information.
    :param threaded: should the process handle each request in a separate
                     thread?
    :param processes: if greater than 1 then handle each request in a new process
                      up to this maximum number of concurrent processes.
    :param request_handler: optional parameter that can be used to replace
                            the default one.  You can use this to replace it
                            with a different
                            :class:`~BaseHTTPServer.BaseHTTPRequestHandler`
                            subclass.
    :param static_files: a list or dict of paths for static files.  This works
                         exactly like :class:`SharedDataMiddleware`, it's actually
                         just wrapping the application in that middleware before
                         serving.
    :param passthrough_errors: set this to `True` to disable the error catching.
                               This means that the server will die on errors but
                               it can be useful to hook debuggers in (pdb etc.)
    :param ssl_context: an SSL context for the connection. Either an
                        :class:`ssl.SSLContext`, a tuple in the form
                        ``(cert_file, pkey_file)``, the string ``'adhoc'`` if
                        the server should automatically create one, or ``None``
                        to disable SSL (which is the default).
    """
    if not isinstance(port, int):
        raise TypeError('port must be an integer')
    if use_debugger:
        from werkzeug.debug import DebuggedApplication
        application = DebuggedApplication(application, use_evalex)
    if static_files:
        from werkzeug.wsgi import SharedDataMiddleware
        application = SharedDataMiddleware(application, static_files)

    def log_startup(sock):
        display_hostname = hostname not in ('', '*') and hostname or 'localhost'
        if ':' in display_hostname:
            display_hostname = '[%s]' % display_hostname
        quit_msg = '(Press CTRL+C to quit)'
        port = sock.getsockname()[1]
        _log('info', ' * Running on %s://%s:%d/ %s',
             ssl_context is None and 'http' or 'https',
             display_hostname, port, quit_msg)
        
## SharedDataMiddleware

    def __call__(self, environ, start_response):
        cleaned_path = get_path_info(environ)
        if PY2:
            cleaned_path = cleaned_path.encode(get_filesystem_encoding())
        # sanitize the path for non unix systems
        cleaned_path = cleaned_path.strip('/')
        for sep in os.sep, os.altsep:
            if sep and sep != '/':
                cleaned_path = cleaned_path.replace(sep, '/')
        path = '/' + '/'.join(x for x in cleaned_path.split('/')
                              if x and x != '..')
        file_loader = None
        for search_path, loader in self.exports:
            if search_path == path:
                real_filename, file_loader = loader(None)
                if file_loader is not None:
                    break
            if not search_path.endswith('/'):
                search_path += '/'
            if path.startswith(search_path):
                real_filename, file_loader = loader(path[len(search_path):])
                if file_loader is not None:
                    break
        if file_loader is None or not self.is_allowed(real_filename):
            return self.app(environ, start_response)

        guessed_type = mimetypes.guess_type(real_filename)
        mime_type = guessed_type[0] or self.fallback_mimetype
        f, mtime, file_size = file_loader()

        headers = [('Date', http_date())]
        if self.cache:
            timeout = self.cache_timeout
            etag = self.generate_etag(mtime, file_size, real_filename)
            headers += [
                ('Etag', '"%s"' % etag),
                ('Cache-Control', 'max-age=%d, public' % timeout)
            ]
            if not is_resource_modified(environ, etag, last_modified=mtime):
                f.close()
                start_response('304 Not Modified', headers)
                return []
            headers.append(('Expires', http_date(time() + timeout)))
        else:
            headers.append(('Cache-Control', 'public'))

        headers.extend((
            ('Content-Type', mime_type),
            ('Content-Length', str(file_size)),
            ('Last-Modified', http_date(mtime))
        ))
        start_response('200 OK', headers)
        return wrap_file(environ, f)

## self.app

 if file_loader is None or not self.is_allowed(real_filename):
            return self.app(environ, start_response)

########################

##当请求进来

     def execute(app):
            application_iter = app(environ, start_response)
            try:
                for data in application_iter:
                    write(data)
                if not headers_sent:
                    write(b'')
            finally:
                if hasattr(application_iter, 'close'):
                    application_iter.close()
                application_iter = None
                
 ## __call__

 def __call__(self, environ, start_response):
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app` which can be
        wrapped to applying middleware."""
        return self.wsgi_app(environ, start_response)
## wsgi_app

 def wsgi_app(self, environ, start_response):
        """The actual WSGI application. This is not implemented in
        :meth:`__call__` so that middlewares can be applied without
        losing a reference to the app object. Instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        .. versionchanged:: 0.7
            Teardown events for the request and app contexts are called
            even if an unhandled error occurs. Other events may not be
            called depending on when an error occurs during dispatch.
            See :ref:`callbacks-and-errors`.

        :param environ: A WSGI environment.
        :param start_response: A callable accepting a status code,
            a list of headers, and an optional exception context to
            start the response.
        """
        ctx = self.request_context(environ)
        error = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)






