package edu.siu.sentiment;

public class ResultRowItem {

	private int posSentiment, negSentiment;
	private String comBody;
	
	public ResultRowItem(int posSentiment, int negSentiment, String comBody){
		this.posSentiment = posSentiment;
		this.negSentiment = negSentiment;
		this.comBody = comBody;
	}
	
	public String getCommentBody(){
		return comBody;
	}
	
	public int getPossitiveSentimentResult(){
		return posSentiment;
	}
	
	public int getNegativeSentimentResult(){
		return negSentiment;
	}
	
}
