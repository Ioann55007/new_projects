
$(function () {
  getTopicReplies();
});

let requestedNewPage = false

$(window).scroll(function () {
  let pagination = $('#replies-list')
  console.log(pagination.height() - $(this).height(), $(this).scrollTop())
  if (pagination.height() - $(this).height() <= $(this).scrollTop() && !requestedNewPage) {
    nextUrl = pagination.attr('data-href-next')
    if (nextUrl && nextUrl != 'None'){
       requestedNewPage = true
       console.log(nextUrl)
    }
  }
});

function getTopicReplies(){
  pagination = $('#paginationReplies')
  url = pagination.attr('data-href-next')
  $.ajax({
   url: url,
   type: 'get',
   success: function (data) {
     console.log('success', data)
     if (data.results) {
        addLinks(pagination, data.next)
        if (renderComments(pagination, data)) {
           requestedNewPage = false;
        }
      }
   },
   error: function (data) {
     console.log('error', data)
   }
  })
}

function addLinks(pagination, next) {
  pagination.attr('data-href-next', next)

}


function renderComments(pagination, data){
  replies = data.results
  console.log(replies)
  $.each(replies, function(i){
    var templateString = `
      <li>
				<div class="comment-main-level">
					<div class="comment-avatar"><img src="http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" alt=""></div>
					<div class="comment-box">
						<div class="comment-head">
							<h6 class="comment-name by-author"><a href="#">${reply[i].author}</a></h6>
							<span>${comments[i].updated}</span>
              <a href="#formReview" onclick="addParentToComment('${replies[i].author}', '${replies[i].id}')"><i class="fa fa-reply"></i></a>
               <i class="fa fa-heart commentLike"
                  data-id="${replis[i].id}" data-vote=1
                  data-href="{% url 'forum:like_topic' %}"da
                  data-type="reply"></i>
						</div>
						<div class="comment-content">
							${replies[i].content}
						</div>
					</div>
				</div>
				<!-- Comments reply -->
				<ul class="comments-list reply-list">
          {% for child in comment.child %}
					<li>
						<div class="comment-avatar"><img src="http://i9.photobucket.com/albums/a88/creaticode/avatar_2_zps7de12f8b.jpg" alt=""></div>

						<div class="comment-box">
							<div class="comment-head">
								<h6 class="comment-name"><a href="#"> {{ child.author }}</a></h6>
								<span>{{ child.updated | date_time }}</span>
                <i class="fa fa-heart commentLike"
                   data-id="{{ child.id }}" data-vote=1
                   data-type="comment" data-href="{% url 'actions:like_topic' %}">
                </i>
							</div>
							<div class="comment-content">
								{{ child.content }}
							</div>
						</div>
					</li>
          {% endfor %}
				</ul>
			</li>

    `
   pagination.append(templateString);
  })
  return true;
}
