/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sentitool;
import uk.ac.wlv.sentistrength.*;

/**
 *
 * @author jacob
 */
public class SentiTool {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        //Method 1: one-off classification (inefficient for multiple classifications)
    //Create an array of command line parameters, including text or file to process
    String ssthInitialisationAndText[] = {"sentidata", "/home/jacob/Development/Undergrad_Research/SentiStrength/SentStrength_Data_Sept2011/", "text", "I+hate+frogs+but+love+dogs.", "explain"};
    SentiStrength.main(ssthInitialisationAndText); 

    //Method 2: One initialisation and repeated classifications
   SentiStrength sentiStrength = new SentiStrength(); 
    //Create an array of command line parameters to send (not text or file to process)
    String ssthInitialisation[] = {"sentidata", "/home/jacob/Development/Undergrad_Research/SentiStrength/SentStrength_Data_Sept2011/", "explain"};
    sentiStrength.initialise(ssthInitialisation); //Initialise
    //can now calculate sentiment scores quickly without having to initialise again
    System.out.println(sentiStrength.computeSentimentScores("I hate frogs.")); 
    System.out.println(sentiStrength.computeSentimentScores("I love dogs.")); 
    }
    
}
