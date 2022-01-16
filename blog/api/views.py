from ..models import Reply, Comment, Likedislike
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .serializers import ReplySerializer

def post(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        reply = Reply(content = data['content'], user=request.user, comment = comment)
        reply.save()
        reply_serializer = ReplySerializer(reply, many=False)
        return JsonResponse({'reply': reply_serializer.data}, status=201)
    replies = comment.reply_set.select_related('user')
    reply_serializer = ReplySerializer(replies, many=True)
    return JsonResponse({'replies': reply_serializer.data}, status=200)

def like_a_post(request, post_id):
    try:
        param = int(request.GET.get('liked'))
    except (ValueError, TypeError):
        return JsonResponse({'message': "Request is not valid"}, status = 400)
    user_id = request.user.id
    
    like = Likedislike.objects.filter(post=post_id, user=user_id).first()
    is_liked = bool(param)
    print(is_liked)
    if like:
        like.liked = is_liked
        like.disliked = not is_liked
        like.save()
    else:
        Likedislike.objects.create(liked=is_liked, disliked=not is_liked, post_id=post_id, user_id=user_id)
    return JsonResponse({'success': True}, status=200)