<?php

class Article
{
	var $tweets;
	var $p_tweets;
	var $n_tweets;
	var $articles;
	var $no_of_tweets;
		
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
			echo $resultData["status"][0][0];
			echo $resultData["positive"][2][0];
			//$art = new Article($resultData);
			$data = $resultData;
			$this->articles = $data["articles"];
			$this->p_tweets = $data["positive"];
			$this->n_tweets = $data["neg"];
			$this->no_of_tweets = $data["no_of_data"];
			
		}
		
	function getTweets()
		{

			$item_head = '<li>
				        <!-- timeline icon -->
				        <i class="fa fa-user bg-aqua"></i>
				        <div class="timeline-item">
				            <span class="time"><i class="fa fa-clock-o"></i> 12:05</span>

				            <h3 class="timeline-header"><a href="#">Bill</a></h3>

				            <div class="timeline-body">';
				                
			$item_tail ='</div>

				        </div>
				    </li>';
			$content = "";
			foreach ($this->p_tweets as $tweet) {
				$content .= $item_head.$tweet.$item_tail;
			}
			foreach ($this->n_tweets as $tweet) {
				$content .= $item_head.$tweet.$item_tail;
			}
			
			return $content;
		}
		function getSummaries()
		{
			$content = "";
			foreach ($this->articles as $tweet) {
				$content .= "<br>".$tweet."</br>";
			}

			return $content;
		}

}
	
?>