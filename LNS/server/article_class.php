<?php

class Article
{
	var $tweets;
	var $p_tweets;
	var $n_tweets;
	var $articles;
	var $p_users;
	var $n_users;
	var $no_tweets;
	var $no_stories;
	var $pnr;
		
	// -- Function Name : __construct
	// -- Params : $ID
	// -- Purpose : 

	function __construct($query)
		{
			set_time_limit(5000);
			error_reporting(E_ALL);
			$python = "/home/d1810/anaconda3/envs/machinelearningpython2/bin/python";
			$python = "/home/rushabh/anaconda2/envs/AI_PROJ/bin/python";
			$codefile = "/home/d1810/Documents/Extra/AI/github/AI_project/src/main.py";
			$codefile = "/home/rushabh/Stony/AI/Project/bbc_dataset/src/main.py";
			$args = $query;

			$ret = 0;
			ob_start();
			// passthru('/usr/bin/python2.7 test.py');
			passthru("$python $codefile $args", $ret);
			$output = ob_get_clean();
			//echo $output;
			$resultData = json_decode($output, true);
			$data = $resultData;
			$this->articles = $data["articles"];
			$this->p_tweets = $data["positive"];
			$this->n_tweets = $data["neg"];
			$this->no_tweets = $data["no_tweets"];
			$this->no_stories = $data["no_stories"];
			$this->n_users = $data["n_users"];
			$this->p_users = $data["p_users"];
			$this->pnr = $data["pnr"];
			
		}
		
	function getTweets()
		{

			$item_header = '<li><i class="fa fa-user bg-aqua"></i>
								<div class="timeline-item">
				            		<span class="time"><i class="fa fa-clock-o"></i>12:05</span>
				            		<h3 class="timeline-header">
				            			<a href="#">';

			$item_main = '</a></h3>';

			$item_trailer = '</div></li>';
			$content = "";
			// var_dump($this->p_tweets);
			// var_dump($this->p_users);
			// var_dump($this->p_tweets);
			// var_dump($this->p_tweets);
			if ((is_array($this->p_tweets) || is_object($this->p_tweets)) && (is_array($this->n_tweets) || is_object($this->n_tweets))) 
			{
				$index = 0;
				foreach ($this->p_tweets as $tweet) {
					$content .= $item_header;
					$content .= $this->p_users[$index];
					$content .= $item_main;
					$content .= $tweet;
					$content .= $item_trailer;
					$index++;
				}
				$index = 0;
				foreach ($this->n_tweets as $tweet) {
					$content .= $item_header;
					$content .= $this->n_users[$index];
					$content .= $item_main;
					$content .= $tweet;
					$content .= $item_trailer;
					$index++;
				}
			}
			return $content;
		}
		function getSummaries()
		{
			$article_head = '<div style="border: 1px solid rgb(238, 238, 238); padding: 5px; margin: 5px;">';
			$article_tail = '</div>';
			$content = "";

			// var_dump($this->articles);
			if (is_array($this->articles) || is_object($this->articles))
			{
				foreach ($this->articles as $article) {
				// echo "ART: <br> $article <br>";
					// $content = "$content $article_head $article $article_tail";
					$content .= $article_head;
					$content .= $article;
					$content .= $article_tail;
				// $content .= $article;
				}
			}
			/*
			foreach ($this->articles as $tweet) {
				$content .= "<br>".$tweet."</br>";
			}
			*/

			return $content;
		}
		function getNoTweets() {
			return $this->no_tweets;
		}

}
	
?>