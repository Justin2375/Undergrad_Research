package edu.siu.sentiment;

import java.sql.ResultSet;
import java.sql.SQLException;

import uk.ac.wlv.sentistrength.SentiStrength;

public class CommentClassifier {
	
	private SentiStrength sentiStrength;
	private DbConnector connect;

	public CommentClassifier(String project){
		connect=new DbConnector("gerrit_"+project);
		sentiStrength = new SentiStrength(); 
		String ssthInitialisation[] = {"sentidata", "./data/","trinary"};
		sentiStrength.initialise(ssthInitialisation); 
		
	}
	
	public void computeInlineComments(){
		ResultSet inlineComments=connect.getAllInlineComments();
		
		int count=0;
		
		try {
			while(inlineComments.next())
			{
				String comment_id=inlineComments.getString(1);
				String message=inlineComments.getString(2);
				
				String[] sentiResult = sentiStrength.computeSentimentScores(message).split("\\s+");
				int rating = Integer.parseInt(sentiResult[2]);
				connect.saveInlineSentimentScore(comment_id, rating);
				count++;
				
				if(count%1000==0)
					System.out.println("Inline comments: "+count);
				
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	public void computeReviewComments(String excludelist){
		ResultSet reviewComments=connect.getAllReviewComments(excludelist);
		int count=0;
		
		try {
			while(reviewComments.next())
			{
				
				String comment_id=reviewComments.getString(1);
				String message=reviewComments.getString(2);
				
				String[] sentiResult = sentiStrength.computeSentimentScores(message).split("\\s+");
				int rating = Integer.parseInt(sentiResult[2]);
				connect.saveReviewSentimentScore(comment_id, rating);
				
				count++;
				if(count%1000==0)
					System.out.println("Review comments: "+count);
				
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	
	public static void main(String[] args) {
		CommentClassifier classifier=new CommentClassifier("kitware");
		classifier.computeInlineComments();
		classifier.computeReviewComments("780,21,775");

	}

}
