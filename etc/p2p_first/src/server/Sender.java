package server;

import java.io.InputStream;
import java.net.Socket;

import packet.ExamplePacket;
import packet.Packet;

public class Sender extends Thread
{
	private Socket socket = null;
	
	public Sender(Socket socket)
	{
		this.socket = socket;
		this.start();
	}
	
	@Override
	public void run()
	{
		try {
			InputStream in = socket.getInputStream();
			while(true)
			{
				if(in.available() > 0)
				{
					// pid ���� �б� (8byte)
					int count = 0;
					byte[] data = new byte[8];
					while(count < 8)
					{
						int r = in.read();
						if(r != -1)
						{
							data[count] = (byte)r;
							count++;
						}
					}
					long pid = Packet.bytesToLong(data);
					
					// type ���� �б� (4byte)
					count = 0;
					data = new byte[4];
					while(count < 4)
					{
						int r = in.read();
						if(r != -1)
						{
							data[count] = (byte)r;
							count++;
						}
					}
					int type = Packet.byteArrayToInt(data);
					
					// bodylength ���� �б� (4byte)
					count = 0;
					data = new byte[4];
					while(count < 4)
					{
						int r = in.read();
						if(r != -1)
						{
							data[count] = (byte)r;
							count++;
						}
					}
					int bodylength = Packet.byteArrayToInt(data);
					
					// body ���� �б� (nbyte)
					count = 0;
					data = new byte[bodylength];
					while(count < bodylength)
					{
						int r = in.read();
						if(r != -1)
						{
							data[count] = (byte)r;
							count++;
						}
					}
					
					// ��밡 ���� byte�� packet���� ��ȯ�Ѵ�.
					Packet pack = new ExamplePacket(pid,type,bodylength,data);
					
					// �ش� packet�� ��� �ִ� �޼����� �д´�.
					System.out.println(pack.toString());
				}
			}
		}catch(Exception e) {
			
		}
		
	}
}
