/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sentitool;
import java.util.Scanner;
import uk.ac.wlv.sentistrength.*;

/**
 *
 * @author jacob
 */
public class SentiTool {

    private static final String SENTI_DATA_PATH = "/home/jacob/Development/"
            + "Undergrad_Research/SentiStrength/SentStrength_Data_Sept2011/"; // String contains the path to the SentiData folder
    private static String mode; // What mode to run as.  Almost always is text.
    private static boolean explainStat; // Flag if the user wants to have the results explained or not
    private Scanner in = new Scanner(System.in); // Scanner for taking in user defined vars
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
    //Method 1: one-off classification (inefficient for multiple classifications)
    //Create an array of command line parameters, including text or file to process
    String ssthInitialisationAndText[] = {"sentidata", SENTI_DATA_PATH, "text", , "explain"};
    SentiStrength.main(ssthInitialisationAndText); 

    //Method 2: One initialisation and repeated classifications
   SentiStrength sentiStrength = new SentiStrength(); 
    //Create an array of command line parameters to send (not text or file to process)
    String ssthInitialisation[] = {"sentidata", SENTI_DATA_PATH, "explain"};
    sentiStrength.initialise(ssthInitialisation); //Initialise
    //can now calculate sentiment scores quickly without having to initialise again
    System.out.println(sentiStrength.computeSentimentScores("I hate frogs.")); 
    System.out.println(sentiStrength.computeSentimentScores("I love dogs.")); 
    }
    
}
