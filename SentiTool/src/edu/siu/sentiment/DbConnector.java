package edu.siu.sentiment;
import java.sql.*;
import java.util.ArrayList;
import java.util.Iterator;

public class DbConnector {
	public Connection connect;

	public DbConnector(String databasename) {

		try {
			Class.forName("com.mysql.jdbc.Driver");
			connect = DriverManager.getConnection("jdbc:mysql://localhost/"
					+ databasename + "?" + "user=softsearch&password=S0ftSe@rch");
		} catch (ClassNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (SQLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}

	}

	public ResultSet getAllInlineComments(){
		try {
			PreparedStatement statement = connect
					.prepareStatement("SELECT comment_id,message from inline_comments WHERE sentiment_score is NULL");
			
			
			
			return statement.executeQuery();

			
		} catch (SQLException e) {

			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;

		
	}
	
	
	public ResultSet getAllReviewComments(String exclude){
		try {
			PreparedStatement statement = connect
					.prepareStatement("SELECT comments_id,message from review_comments "+
							" WHERE sentiment_score is NULL and author not in ("+exclude+")");
			
			
			
			return statement.executeQuery();

			
		} catch (SQLException e) {

			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;

		
	}

	
	public boolean saveInlineSentimentScore(String comment_id,int score) {
		try {
			PreparedStatement statement = connect
					.prepareStatement("UPDATE inline_comments SET sentiment_score=? WHERE comment_id=?");
			
			statement.setInt(1, score);
			statement.setString(2, comment_id);
			
			statement.executeUpdate();

			return true;
		} catch (SQLException e) {

			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return false;

	}
	
	public boolean saveReviewSentimentScore(String comment_id,int score) {
		try {
			PreparedStatement statement = connect
					.prepareStatement("UPDATE review_comments SET sentiment_score=? WHERE comments_id=?");
			
			statement.setInt(1, score);
			statement.setString(2, comment_id);
			
			statement.executeUpdate();

			return true;
		} catch (SQLException e) {

			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return false;

	}

	
}
