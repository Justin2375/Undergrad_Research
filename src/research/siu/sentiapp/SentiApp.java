package research.siu.sentiapp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;
import uk.ac.wlv.sentistrength.*;

public class SentiApp {

	/**
	 * @param args
	 */
	
	private static String input = " ";
	private static final BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
	
	public static void main(String[] args) {
		// TODO Auto-generated method s
		try {
			while(input != null){
				input = stdin.readLine();
				System.out.println(input);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
