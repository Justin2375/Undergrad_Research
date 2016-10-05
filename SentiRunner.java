/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sentirunner;
import java.util.Scanner;
import uk.ac.wlv.sentistrength.*;

/**
 *
 * @author jacobreed
 */
public class SentiRunner {

    /**
     * @param args the command line arguments
     */
    private static Scanner in = new Scanner(System.in);
    private static String filePath;
    private static String mode;
    private static final String SENTIDATAPATH = "/Users/jacobreed/Desktop/SentiStrength";
    
    public static void main(String[] args) {
        System.out.println("Enter a filepath for the text to be examined:");
        filePath = in.nextLine(); // Filpath where the document to be tested lives 
        
        System.out.println("Enter the mode:"); // Mode to use with SentiStrength
        mode = in.nextLine();
        
        String ssthInitialiaztionAndText[] = {"sentidata",
            SENTIDATAPATH, mode, filePath}; // Array houses the command to run with SentiStrength
        
        SentiStrength.main(ssthInitialiaztionAndText); // Runs with the given string array
        
        
        // SentiStrength classifier = new SentiStrength();
        // SentiStrength classifier2 = new SentiStrength();
        
        
    }
    
}
