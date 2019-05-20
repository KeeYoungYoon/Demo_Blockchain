package client;

import java.io.OutputStream;
import java.net.Socket;
import java.util.Scanner;

import packet.ExamplePacket;
import packet.Game;
import packet.Packet;

public class Client 
{
	public static void main(String[] args)
	{
		try {
			// 1. ������ �����ϱ� 
			Socket server = new Socket("127.0.0.1",9099);
			
			// 2. Packet�� �������
			//Packet packet = new ExamplePacket("sissor");
            String msg;
            Scanner scan = new Scanner(System.in);
            System.out.println("����,����,�� ���� �ϳ��� �Է��ϼ���");
            msg = scan.nextLine();

			Packet packet = new Game(msg);
			
			// 3. �������� packet�� ��������
			OutputStream out = server.getOutputStream();
			out.write(packet.getBytes());
			
			// 4. �������Լ� ������ �ޱ�
			while(true)
			{
				// ~~~
			}
		}catch(Exception e) {
			
		}
	}
}
