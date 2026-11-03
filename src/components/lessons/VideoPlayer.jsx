import React, { useState } from 'react';
import { getYouTubeEmbedUrl, extractYouTubeVideoId } from '../../utils/youtube';
import { Play, ExternalLink, VideoOff } from 'lucide-react';
import { Button } from '../common/Button';

export const VideoPlayer = ({ videoUrl, title = 'Video Lesson' }) => {
  const [hasError, setHasError] = useState(false);
  const embedUrl = getYouTubeEmbedUrl(videoUrl);
  const videoId = extractYouTubeVideoId(videoUrl);

  if (!videoUrl || !embedUrl || hasError) {
    return (
      <div className="w-full aspect-video rounded-2xl bg-slate-100 border border-slate-200 flex flex-col items-center justify-center p-6 text-center">
        <div className="w-12 h-12 rounded-xl bg-slate-200 text-slate-400 flex items-center justify-center mb-3">
          <VideoOff className="w-6 h-6" />
        </div>
        <h4 className="text-sm font-semibold text-slate-700 mb-1">
          {videoUrl ? 'Video Stream Unavailable' : 'No Video Attached to this Lesson'}
        </h4>
        <p className="text-xs text-slate-500 max-w-sm mb-4">
          {videoUrl
            ? (videoId ? 'The video could not be embedded directly. You can try watching on YouTube.' : 'This video URL is unsupported or unsafe. Ask an administrator to replace it.')
            : 'Study the structured learning material, vocabulary flashcards, and take the quiz below.'}
        </p>
        {videoId && (
          <a
            href={`https://www.youtube.com/watch?v=${videoId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-semibold transition-colors"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            Watch on YouTube
          </a>
        )}
      </div>
    );
  }

  return (
    <div className="w-full space-y-2">
      <div className="relative w-full aspect-video rounded-2xl overflow-hidden bg-slate-900 shadow-soft-lg border border-slate-200">
        <iframe
          src={embedUrl}
          title={title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
          onError={() => setHasError(true)}
          className="absolute inset-0 w-full h-full border-0"
        />
      </div>
      <div className="flex items-center justify-between text-xs text-slate-500 px-1">
        <span className="font-medium">Educational Video Tutorial</span>
        {videoId && (
          <a
            href={`https://www.youtube.com/watch?v=${videoId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-brand-600 hover:text-brand-700 font-semibold"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            Open in YouTube
          </a>
        )}
      </div>
    </div>
  );
};
