package edu.siu.sentiment;

public class RatedComment {

	private int rating;
	private String comments;
	
	/**
	 * This method will be used to return the sentiment rating 
	 * of each of the evaluated comments.
	 * @return The sentiment rating of the comment
	 */
	public int getRating() {
		return rating;
	}

	/**
	 * Retrieves the comment from the spreadsheet where
	 * all of the comments and final ratings are stored
	 * at. 
	 * @return
	 */
	public String getComments() {
		return comments;
	}
	
	/**
	 * Constructor for each of the scraped comments.
	 * Each comment will be of this object type which
	 * will store the comment and it's final rating.
	 * @param comments The body of the comment
	 * @param rating The final rating of the comment 
	 */
	public RatedComment(String comments, int rating){
		this.comments = comments;
		this.rating = rating;
	}
	
}
