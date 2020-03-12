flask源码分析
## https://cizixs.com/2017/01/13/flask-insight-context/

所有的 python web 框架都要遵循 WSGI 协议，如果对 WSGI 不清楚，可以查看我之前的介绍文章。

在这里还是要简单回顾一下 WSGI 的核心概念。

WSGI 中有一个非常重要的概念：每个 python web 应用都是一个可调用（callable）的对象。在 flask 中，\
这个对象就是 app = Flask(__name__) 创建出来的 app，就是下图中的绿色 Application 部分。要运行 web 应用，\
必须有 web server，比如我们熟悉的 apache、nginx ，或者 python 中的 gunicorn ，\
我们下面要讲到的 werkzeug 提供的 WSGIServer，它们是下图的黄色 Server 部分。

Server 和 Application 之间怎么通信，就是 WSGI 的功能。它规定了 app(environ, start_response) 的接口，\
server 会调用 application，并传给它两个参数：environ 包含了请求的所有信息，start_response 是 application 
处理完之后需要调用的函数，参数是状态码、响应头部还有错误信息。

WSGI application 非常重要的特点是：它是可以嵌套的。换句话说，我可以写个 application，\
它做的事情就是调用另外一个 application，然后再返回（类似一个 proxy）。一般来说，嵌套的最后一层是业务应用，\
中间就是 middleware。这样的好处是，可以解耦业务逻辑和其他功能，比如限流、认证、序列化等都实现成不同的中间层，\
不同的中间层和业务逻辑是不相关的，可以独立维护；而且用户也可以动态地组合不同的中间层来满足不同的需求。

这里的 app = Flask(__name__) 就是上面提到的 Application 部分，但是我们并没有看到 Server 的部分，那么它一定是隐藏到 app.run() 内部某个地方了。
