import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useLearning } from '../../contexts/LearningContext';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';
import { Modal } from '../../components/common/Modal';
import { ConfirmDialog } from '../../components/common/ConfirmDialog';
import { ErrorMessage } from '../../components/common/ErrorMessage';
import { LoadingState } from '../../components/common/LoadingState';
import { Link, useNavigate } from 'react-router-dom';
import { isValidYouTubeUrl } from '../../utils/youtube';
import {
  BookOpen,
  Plus,
  Edit2,
  Trash2,
  Video,
  SpellCheck,
  HelpCircle,
  ExternalLink,
  Eye,
  Filter
} from 'lucide-react';

export const ManageLessonsPage = () => {
  const navigate = useNavigate();
  const { languages, levels, refreshData } = useLearning();
  const [courses,setCourses]=useState([]);
  const [modules,setModules]=useState([]);
  useEffect(()=>{Promise.all([api.adminList('courses'),api.adminList('modules')]).then(([c,m])=>{setCourses(c);setModules(m)}).catch(e=>setError(e.message));},[]);

  const [selectedLanguageId, setSelectedLanguageId] = useState('');
  const [selectedLevelId, setSelectedLevelId] = useState('');
  const [lessons, setLessons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentId, setCurrentId] = useState(null);

  // Form State
  const [formData, setFormData] = useState({
    language_id: '',
    level_id: '',
    module_id: '',
    title: '',
    description: '',
    duration_minutes: 15,
    lesson_order: 1,
    objectives: '',
    video_url: '',
    content: '',
    grammar_notes: '',
    is_published: true
  });
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  // Delete Dialog
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    if (languages.length > 0 && !selectedLanguageId) {
      setSelectedLanguageId(languages[0].id);
    }
    if (levels.length > 0 && !selectedLevelId) {
      setSelectedLevelId(levels[0].id);
    }
  }, [languages, levels]);

  const fetchLessons = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const all = await api.adminList('lessons');
      const data = all.filter(l => (!selectedLanguageId || l.language_id===selectedLanguageId) && (!selectedLevelId || l.level_id===selectedLevelId));
      setLessons(data || []);
    } catch (err) {
      setError(err.message || 'Failed to load lessons');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedLanguageId && selectedLevelId) {
      fetchLessons();
    }
  }, [selectedLanguageId, selectedLevelId]);

  const handleOpenAdd = () => {
    setFormData({
      language_id: selectedLanguageId || languages[0]?.id || '',
      level_id: selectedLevelId || levels[0]?.id || '',
      module_id: '',
      title: '',
      description: '',
      duration_minutes: 15,
      lesson_order: lessons.length + 1,
      objectives: '',
      video_url: '',
      content: '',
      grammar_notes: '',
      is_published: true
    });
    setIsEditing(false);
    setCurrentId(null);
    setFormError('');
    setIsModalOpen(true);
  };

  const handleOpenEdit = (lesson) => {
    setFormData({
      language_id: lesson.language_id,
      level_id: lesson.level_id,
      module_id: lesson.module_id,
      title: lesson.title,
      description: lesson.description || '',
      duration_minutes: lesson.duration_minutes || 15,
      lesson_order: lesson.lesson_order || 1,
      objectives: Array.isArray(lesson.objectives) ? lesson.objectives.join('\n') : (lesson.objectives || ''),
      video_url: lesson.video_url || '',
      content: lesson.content || '',
      grammar_notes: lesson.grammar_notes || '',
      is_published: lesson.is_published ?? true
    });
    setIsEditing(true);
    setCurrentId(lesson.id);
    setFormError('');
    setIsModalOpen(true);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!formData.module_id) {setFormError('Select a course module for the lesson.');return;}
    if (!formData.title || !formData.content) {
      setFormError('Lesson title and explanatory content are required.');
      return;
    }

    if (!isValidYouTubeUrl(formData.video_url.trim())) {
      setFormError('Video must be a supported HTTPS YouTube URL (or left blank).');
      return;
    }
    try {
      setFormSubmitting(true);
      setFormError('');

      const payload = {
        ...formData,
        video_url: formData.video_url.trim(),
        duration_minutes: Number(formData.duration_minutes) || 15,
        lesson_order: Number(formData.lesson_order) || 1,
        objectives: formData.objectives.split('\n').filter(o => o.trim() !== '')
      };

      if (isEditing) {
        await api.updateLesson(currentId, payload);
      } else {
        await api.createLesson(payload);
      }

      setIsModalOpen(false);
      await fetchLessons();
      await refreshData();
    } catch (err) {
      setFormError(err.message || 'Failed to save lesson.');
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleTogglePublish = async (lesson) => {
    try {
      await api.updateLesson(lesson.id, { is_published: !lesson.is_published });
      await fetchLessons();
      await refreshData();
    } catch (err) {
      setError(err.message || 'Failed to toggle publication status.');
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      await api.deleteLesson(deletingId);
      setDeleteDialogOpen(false);
      setDeletingId(null);
      await fetchLessons();
      await refreshData();
    } catch (err) {
      setError(err.message || 'Failed to delete lesson.');
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-purple-600" />
            Manage Lessons
          </h1>
          <p className="text-xs text-slate-500">
            Create, organize, and publish educational lessons for any language & level.
          </p>
        </div>

        <Button onClick={handleOpenAdd} variant="primary" size="sm" icon={Plus}>
          Create New Lesson
        </Button>
      </div>

      <ErrorMessage message={error} />

      {/* Filters Bar */}
      <Card className="p-4 flex flex-wrap items-center gap-4 bg-white">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-bold text-slate-700 uppercase">Filter Curricula:</span>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs font-medium text-slate-500">Language:</label>
          <select
            value={selectedLanguageId}
            onChange={(e) => setSelectedLanguageId(e.target.value)}
            className="px-3 py-1.5 rounded-xl border border-slate-300 text-xs font-semibold text-slate-800 focus:ring-2 focus:ring-purple-500 bg-white"
          >
            {languages.map((lang) => (
              <option key={lang.id} value={lang.id}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs font-medium text-slate-500">CEFR Level:</label>
          <select
            value={selectedLevelId}
            onChange={(e) => setSelectedLevelId(e.target.value)}
            className="px-3 py-1.5 rounded-xl border border-slate-300 text-xs font-semibold text-slate-800 focus:ring-2 focus:ring-purple-500 bg-white"
          >
            {levels.map((lvl) => (
              <option key={lvl.id} value={lvl.id}>
                {lvl.code} ({lvl.name})
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* Lessons Table */}
      {isLoading ? (
        <LoadingState message="Loading curriculum lessons..." />
      ) : (
        <Card className="p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 text-slate-700 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-4 text-center">Order</th>
                  <th className="py-3.5 px-6">Lesson Title</th>
                  <th className="py-3.5 px-4 text-center">Duration</th>
                  <th className="py-3.5 px-4 text-center">Video</th>
                  <th className="py-3.5 px-4 text-center">Status</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {lessons.map((lesson) => (
                  <tr key={lesson.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-4 px-4 text-center font-bold text-brand-700">
                      #{lesson.lesson_order}
                    </td>
                    <td className="py-4 px-6">
                      <p className="font-bold text-slate-900 text-sm font-devanagari">
                        {lesson.title}
                      </p>
                      <p className="text-xs text-slate-500 max-w-sm truncate font-devanagari">
                        {lesson.description || 'No description provided'}
                      </p>
                    </td>
                    <td className="py-4 px-4 text-center font-medium text-slate-600">
                      {lesson.duration_minutes || 15}m
                    </td>
                    <td className="py-4 px-4 text-center">
                      {lesson.video_url ? (
                        <Badge variant="success" size="sm">
                          <Video className="w-3 h-3 text-emerald-600" />
                          Attached
                        </Badge>
                      ) : (
                        <span className="text-slate-400 italic">None</span>
                      )}
                    </td>
                    <td className="py-4 px-4 text-center">
                      <button
                        onClick={() => handleTogglePublish(lesson)}
                        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold transition-colors ${
                          lesson.is_published
                            ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200'
                            : 'bg-amber-50 text-amber-700 hover:bg-amber-100 border border-amber-200'
                        }`}
                      >
                        {lesson.is_published ? 'Published' : 'Draft'}
                      </button>
                    </td>
                    <td className="py-4 px-6 text-right space-x-2">
                      <Link
                        to={`/lesson/${lesson.id}`}
                        target="_blank"
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-600 font-semibold"
                        title="Preview in Student View"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        Preview
                      </Link>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleOpenEdit(lesson)}
                        icon={Edit2}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setDeletingId(lesson.id);
                          setDeleteDialogOpen(true);
                        }}
                        className="text-rose-600 hover:bg-rose-50"
                        icon={Trash2}
                      >
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))}
                {lessons.length === 0 && (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-slate-400">
                      No lessons found for this language and level combination. Click "Create New Lesson" above to add one.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Add / Edit Lesson Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={isEditing ? 'Edit Lesson' : 'Create New Lesson'}
        maxWidth="max-w-2xl"
      >
        <form onSubmit={handleFormSubmit} className="space-y-4">
          <ErrorMessage message={formError} />

          <label className="block text-xs font-bold text-slate-700">Assign to a specific course module
            <select required className="block mt-2 border rounded-xl p-3 w-full" value={formData.module_id||''} onChange={e=>setFormData({...formData,module_id:e.target.value})}>
              <option value="">Select course and module</option>
              {courses.filter(c=>c.language_id===formData.language_id&&c.level_id===formData.level_id).flatMap(c=>modules.filter(m=>m.course_id===c.id).map(m=><option key={m.id} value={m.id}>{c.title} → {m.title}</option>))}
            </select>
          </label>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Language
              </label>
              <select
                value={formData.language_id}
                onChange={(e) => setFormData({ ...formData, language_id: e.target.value, module_id: '' })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500 bg-white"
              >
                {languages.map((l) => (
                  <option key={l.id} value={l.id}>{l.flag} {l.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                CEFR Level
              </label>
              <select
                value={formData.level_id}
                onChange={(e) => setFormData({ ...formData, level_id: e.target.value, module_id: '' })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500 bg-white"
              >
                {levels.map((lvl) => (
                  <option key={lvl.id} value={lvl.id}>{lvl.code} - {lvl.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="col-span-2">
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Lesson Title
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Greetings & Introductions"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Order (#)
              </label>
              <input
                type="number"
                min={1}
                required
                value={formData.lesson_order}
                onChange={(e) => setFormData({ ...formData, lesson_order: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Duration (minutes)
              </label>
              <input
                type="number"
                min={5}
                max={120}
                value={formData.duration_minutes}
                onChange={(e) => setFormData({ ...formData, duration_minutes: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                YouTube Video URL (Optional)
              </label>
              <input
                type="url"
                placeholder="https://www.youtube.com/watch?v=..."
                value={formData.video_url}
                onChange={(e) => setFormData({ ...formData, video_url: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Short Description
            </label>
            <textarea
              rows={2}
              placeholder="Brief summary of this lesson..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Learning Objectives (One per line)
            </label>
            <textarea
              rows={2}
              placeholder="Master polite daytime greetings&#10;Introduce yourself with name and country"
              value={formData.objectives}
              onChange={(e) => setFormData({ ...formData, objectives: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Grammar Notes (Tip Box)
            </label>
            <textarea
              rows={2}
              placeholder="e.g. In Marathi, nouns change form based on gender and number..."
              value={formData.grammar_notes}
              onChange={(e) => setFormData({ ...formData, grammar_notes: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Explanatory Lesson Content (Markdown Supported)
            </label>
            <textarea
              rows={5}
              required
              placeholder="### Welcome to the lesson&#10;Explain grammar, sentence structures, and dialogues here..."
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500 font-mono"
            />
          </div>

          <div className="flex items-center gap-2 pt-2">
            <input
              type="checkbox"
              id="is_published_check"
              checked={formData.is_published}
              onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
              className="rounded text-purple-600 focus:ring-purple-500"
            />
            <label htmlFor="is_published_check" className="text-xs font-semibold text-slate-700">
              Publish immediately for learners
            </label>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" isLoading={formSubmitting}>
              {isEditing ? 'Save Changes' : 'Publish Lesson'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Lesson"
        message="Are you sure you want to delete this lesson? All student progress, vocabulary items, and quizzes for this lesson will be permanently removed."
      />
    </div>
  );
};
