package server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Receiver extends Thread
{
	private ServerSocket server = null;
	private static Receiver instance = null;
	private Sender client = null;
	
	private Receiver()
	{
		try {
			server = new ServerSocket(9099);
			this.start();
		}catch(Exception e) {
			System.out.println("������ 2���̻� �� �� �����ϴ�.");
		}
	}
	
	public static Receiver getInstance() {
		if(instance == null) {
			instance = new Receiver();
		}
		return instance;
	}
			
	
	@Override
	public void run()
	{
		while(true)
		{
			try {
				client = new Sender(server.accept());
			} catch (Exception e) {
				System.out.println("Ŭ���̾�Ʈ�� �������ӿ� �����Ͽ����ϴ�.");
			}
		}
	}
}
