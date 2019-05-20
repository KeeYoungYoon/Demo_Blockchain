package main;

import java.net.InetSocketAddress;

import org.apache.mina.core.future.ConnectFuture;
import org.apache.mina.core.service.IoHandler;
import org.apache.mina.core.session.IoSession;
import org.apache.mina.filter.codec.ProtocolCodecFilter;

public class client {
	
	public client() {
		connector.setConnectTimeoutMillis(15 * 1000);

		connector.getFilterChain().addLast("codec", new ProtocolCodecFilter(textLineCodecFactory));

		connector.setHandler(new handler()); // �ڵ鷯�� ��������� �Ѵ�.

		ConnectFuture future = connector.connect(new InetSocketAddress("127.0.0.1", 8080)); // ���� ����

		future.awaitUninterruptibly(); // ���� ��ٸ�

		IoSession session = future.getSession(); // ���ӵǸ� ������ ������

		session.getCloseFuture().awaitUninterruptibly(); // ������ ���� ������ ��ٸ�

		connector.dispose(); // ������ ������
	}
}
