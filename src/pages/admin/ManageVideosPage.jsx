import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useLearning } from '../../contexts/LearningContext';
import { VideoPlayer } from '../../components/lessons/VideoPlayer';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';
import { Modal } from '../../components/common/Modal';
import { ErrorMessage } from '../../components/common/ErrorMessage';
import { LoadingState } from '../../components/common/LoadingState';
import { Video, Edit2, Filter, ExternalLink, PlayCircle } from 'lucide-react';
import { isValidYouTubeUrl } from '../../utils/youtube';

export const ManageVideosPage = () => {
  const { languages, allLessons, refreshData } = useLearning();

  const [selectedLanguageId, setSelectedLanguageId] = useState('');
  const [lessons, setLessons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Quick Edit Modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingLesson, setEditingLesson] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (languages.length > 0 && !selectedLanguageId) {
      setSelectedLanguageId(languages[0].id);
    }
  }, [languages]);

  const fetchLessons = async () => {
    try {
      setIsLoading(true);
      const data = await api.getLessons({
        language_id: selectedLanguageId || undefined
      });
      setLessons(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedLanguageId) {
      fetchLessons();
    }
  }, [selectedLanguageId]);

  const handleOpenEdit = (lesson) => {
    setEditingLesson(lesson);
    setVideoUrl(lesson.video_url || '');
    setError('');
    setIsModalOpen(true);
  };

  const handleSaveVideo = async (e) => {
    e.preventDefault();
    if (!isValidYouTubeUrl(videoUrl.trim())) {
      setError('Enter a supported HTTPS YouTube video link, or leave the field empty to remove it.');
      return;
    }
    try {
      setIsSubmitting(true);
      setError('');
      await api.updateLesson(editingLesson.id, { video_url: videoUrl.trim() });
      setIsModalOpen(false);
      await fetchLessons();
      await refreshData();
    } catch (err) {
      setError(err.message || 'Failed to update video URL');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2">
            <Video className="w-6 h-6 text-purple-600" />
            Manage Video Lessons
          </h1>
          <p className="text-xs text-slate-500">
            Audit, test, and update embedded educational YouTube tutorials across all lessons.
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <Card className="p-4 flex items-center gap-4 bg-white">
        <Filter className="w-4 h-4 text-slate-400" />
        <span className="text-xs font-bold text-slate-700 uppercase">Language:</span>
        <select
          value={selectedLanguageId}
          onChange={(e) => setSelectedLanguageId(e.target.value)}
          className="px-3 py-1.5 rounded-xl border border-slate-300 text-xs font-semibold text-slate-800 bg-white"
        >
          {languages.map((l) => (
            <option key={l.id} value={l.id}>{l.flag} {l.name}</option>
          ))}
        </select>
      </Card>

      {/* Lessons Video Grid */}
      {isLoading ? (
        <LoadingState message="Loading video resources..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {lessons.map((lesson) => (
            <Card key={lesson.id} className="p-6 space-y-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="primary" size="sm">Lesson #{lesson.lesson_order}</Badge>
                    {lesson.video_url ? (
                      <Badge variant="success" size="sm">Embedded</Badge>
                    ) : (
                      <Badge variant="default" size="sm">No Video</Badge>
                    )}
                  </div>
                  <h3 className="text-base font-bold text-slate-900 font-devanagari">
                    {lesson.title}
                  </h3>
                </div>

                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleOpenEdit(lesson)}
                  icon={Edit2}
                >
                  Edit Video URL
                </Button>
              </div>

              {/* Video Player Preview */}
              <div className="pt-2">
                <VideoPlayer videoUrl={lesson.video_url} title={lesson.title} />
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Edit Video Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Update Lesson Video Tutorial"
      >
        <form onSubmit={handleSaveVideo} className="space-y-4">
          <ErrorMessage message={error} />

          <p className="text-xs text-slate-600">
            Editing video tutorial for: <b>{editingLesson?.title}</b>
          </p>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              YouTube Video Link or Embed URL
            </label>
            <input
              type="url"
              placeholder="https://www.youtube.com/watch?v=..."
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
            />
            <span className="text-[11px] text-slate-400 mt-1 block">
              Supports standard YouTube URLs (e.g. watch?v=, youtu.be, embed/). Leave blank if no video is available.
            </span>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={isSubmitting} isLoading={isSubmitting}>
              Save Video URL
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
