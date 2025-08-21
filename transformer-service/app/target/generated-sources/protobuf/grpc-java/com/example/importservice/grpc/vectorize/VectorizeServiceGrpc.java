package com.example.importservice.grpc.vectorize;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.grpc.stub.annotations.GrpcGenerated
public final class VectorizeServiceGrpc {

  private VectorizeServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "importservice.VectorizeService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.example.importservice.grpc.vectorize.VectorizeRequest,
      com.example.importservice.grpc.vectorize.VectorizeResponse> getGetEmbeddingVectorMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetEmbeddingVector",
      requestType = com.example.importservice.grpc.vectorize.VectorizeRequest.class,
      responseType = com.example.importservice.grpc.vectorize.VectorizeResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.example.importservice.grpc.vectorize.VectorizeRequest,
      com.example.importservice.grpc.vectorize.VectorizeResponse> getGetEmbeddingVectorMethod() {
    io.grpc.MethodDescriptor<com.example.importservice.grpc.vectorize.VectorizeRequest, com.example.importservice.grpc.vectorize.VectorizeResponse> getGetEmbeddingVectorMethod;
    if ((getGetEmbeddingVectorMethod = VectorizeServiceGrpc.getGetEmbeddingVectorMethod) == null) {
      synchronized (VectorizeServiceGrpc.class) {
        if ((getGetEmbeddingVectorMethod = VectorizeServiceGrpc.getGetEmbeddingVectorMethod) == null) {
          VectorizeServiceGrpc.getGetEmbeddingVectorMethod = getGetEmbeddingVectorMethod =
              io.grpc.MethodDescriptor.<com.example.importservice.grpc.vectorize.VectorizeRequest, com.example.importservice.grpc.vectorize.VectorizeResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetEmbeddingVector"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.example.importservice.grpc.vectorize.VectorizeRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.example.importservice.grpc.vectorize.VectorizeResponse.getDefaultInstance()))
              .setSchemaDescriptor(new VectorizeServiceMethodDescriptorSupplier("GetEmbeddingVector"))
              .build();
        }
      }
    }
    return getGetEmbeddingVectorMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static VectorizeServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceStub>() {
        @java.lang.Override
        public VectorizeServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new VectorizeServiceStub(channel, callOptions);
        }
      };
    return VectorizeServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports all types of calls on the service
   */
  public static VectorizeServiceBlockingV2Stub newBlockingV2Stub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceBlockingV2Stub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceBlockingV2Stub>() {
        @java.lang.Override
        public VectorizeServiceBlockingV2Stub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new VectorizeServiceBlockingV2Stub(channel, callOptions);
        }
      };
    return VectorizeServiceBlockingV2Stub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static VectorizeServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceBlockingStub>() {
        @java.lang.Override
        public VectorizeServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new VectorizeServiceBlockingStub(channel, callOptions);
        }
      };
    return VectorizeServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static VectorizeServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<VectorizeServiceFutureStub>() {
        @java.lang.Override
        public VectorizeServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new VectorizeServiceFutureStub(channel, callOptions);
        }
      };
    return VectorizeServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void getEmbeddingVector(com.example.importservice.grpc.vectorize.VectorizeRequest request,
        io.grpc.stub.StreamObserver<com.example.importservice.grpc.vectorize.VectorizeResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetEmbeddingVectorMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service VectorizeService.
   */
  public static abstract class VectorizeServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return VectorizeServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service VectorizeService.
   */
  public static final class VectorizeServiceStub
      extends io.grpc.stub.AbstractAsyncStub<VectorizeServiceStub> {
    private VectorizeServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected VectorizeServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new VectorizeServiceStub(channel, callOptions);
    }

    /**
     */
    public void getEmbeddingVector(com.example.importservice.grpc.vectorize.VectorizeRequest request,
        io.grpc.stub.StreamObserver<com.example.importservice.grpc.vectorize.VectorizeResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetEmbeddingVectorMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service VectorizeService.
   */
  public static final class VectorizeServiceBlockingV2Stub
      extends io.grpc.stub.AbstractBlockingStub<VectorizeServiceBlockingV2Stub> {
    private VectorizeServiceBlockingV2Stub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected VectorizeServiceBlockingV2Stub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new VectorizeServiceBlockingV2Stub(channel, callOptions);
    }

    /**
     */
    public com.example.importservice.grpc.vectorize.VectorizeResponse getEmbeddingVector(com.example.importservice.grpc.vectorize.VectorizeRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetEmbeddingVectorMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do limited synchronous rpc calls to service VectorizeService.
   */
  public static final class VectorizeServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<VectorizeServiceBlockingStub> {
    private VectorizeServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected VectorizeServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new VectorizeServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public com.example.importservice.grpc.vectorize.VectorizeResponse getEmbeddingVector(com.example.importservice.grpc.vectorize.VectorizeRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetEmbeddingVectorMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service VectorizeService.
   */
  public static final class VectorizeServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<VectorizeServiceFutureStub> {
    private VectorizeServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected VectorizeServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new VectorizeServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.example.importservice.grpc.vectorize.VectorizeResponse> getEmbeddingVector(
        com.example.importservice.grpc.vectorize.VectorizeRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetEmbeddingVectorMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_GET_EMBEDDING_VECTOR = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_GET_EMBEDDING_VECTOR:
          serviceImpl.getEmbeddingVector((com.example.importservice.grpc.vectorize.VectorizeRequest) request,
              (io.grpc.stub.StreamObserver<com.example.importservice.grpc.vectorize.VectorizeResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getGetEmbeddingVectorMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.example.importservice.grpc.vectorize.VectorizeRequest,
              com.example.importservice.grpc.vectorize.VectorizeResponse>(
                service, METHODID_GET_EMBEDDING_VECTOR)))
        .build();
  }

  private static abstract class VectorizeServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    VectorizeServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.example.importservice.grpc.vectorize.VectorizeProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("VectorizeService");
    }
  }

  private static final class VectorizeServiceFileDescriptorSupplier
      extends VectorizeServiceBaseDescriptorSupplier {
    VectorizeServiceFileDescriptorSupplier() {}
  }

  private static final class VectorizeServiceMethodDescriptorSupplier
      extends VectorizeServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    VectorizeServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (VectorizeServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new VectorizeServiceFileDescriptorSupplier())
              .addMethod(getGetEmbeddingVectorMethod())
              .build();
        }
      }
    }
    return result;
  }
}
