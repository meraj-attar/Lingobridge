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
import {
  SpellCheck,
  Plus,
  Trash2,
  Filter,
  BookOpen,
  Sparkles
} from 'lucide-react';

export const ManageVocabularyPage = () => {
  const { languages, allLessons } = useLearning();

  const [selectedLanguageId, setSelectedLanguageId] = useState('');
  const [selectedLessonId, setSelectedLessonId] = useState('');
  const [currentLesson, setCurrentLesson] = useState(null);
  const [vocabulary, setVocabulary] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId,setEditingId]=useState(null);
  const [formData, setFormData] = useState({
    word: '',
    translation: '',
    pronunciation: '',
    example_sentence: '',
    example_translation: ''
  });
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  // Delete State
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    if (languages.length > 0 && !selectedLanguageId) {
      setSelectedLanguageId(languages[0].id);
    }
  }, [languages]);

  const langLessons = allLessons.filter(l => l.language_id === selectedLanguageId);

  useEffect(() => {
    if (langLessons.length > 0) {
      setSelectedLessonId(langLessons[0].id);
    } else {
      setSelectedLessonId('');
    }
  }, [selectedLanguageId]);

  const loadLessonVocabulary = async () => {
    if (!selectedLessonId) {
      setVocabulary([]);
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const data = await api.getLessonById(selectedLessonId);
      setCurrentLesson(data);
      setVocabulary(data.vocabulary_items || data.vocabulary || []);
    } catch (err) {
      setError(err.message || 'Failed to load vocabulary');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadLessonVocabulary();
  }, [selectedLessonId]);

  const handleOpenAdd = () => {
    setEditingId(null);
    setFormData({
      word: '',
      translation: '',
      pronunciation: '',
      example_sentence: '',
      example_translation: ''
    });
    setFormError('');
    setIsModalOpen(true);
  };

  const handleOpenEdit = item => {
    setEditingId(item.id);
    setFormData({word:item.word||'',translation:item.translation||'',pronunciation:item.pronunciation||'',example_sentence:item.example_sentence||'',example_translation:item.example_translation||''});
    setFormError('');setIsModalOpen(true);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!formData.word || !formData.translation) {
      setFormError('Word and translation are mandatory.');
      return;
    }

    try {
      setFormSubmitting(true);
      setFormError('');
      if(editingId)await api.adminUpdate('vocabulary',editingId,formData);
      else await api.addVocabularyItem(selectedLessonId, formData);
      setIsModalOpen(false);
      await loadLessonVocabulary();
    } catch (err) {
      setFormError(err.message || 'Failed to add vocabulary word.');
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      await api.deleteVocabularyItem(selectedLessonId, deletingId);
      setDeleteDialogOpen(false);
      setDeletingId(null);
      await loadLessonVocabulary();
    } catch (err) {
      setError(err.message || 'Failed to delete vocabulary item.');
    }
  };

  const selectedLang = languages.find(l => l.id === selectedLanguageId);

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2">
            <SpellCheck className="w-6 h-6 text-purple-600" />
            Manage Vocabulary
          </h1>
          <p className="text-xs text-slate-500">
            Add words, translations, pronunciation phonetics, and sample bilingual sentences.
          </p>
        </div>

        <Button
          onClick={handleOpenAdd}
          variant="primary"
          size="sm"
          disabled={!selectedLessonId}
          icon={Plus}
        >
          Add Vocabulary Word
        </Button>
      </div>

      <ErrorMessage message={error} />

      {/* Selectors */}
      <Card className="p-4 flex flex-wrap items-center gap-4 bg-white">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-bold text-slate-700 uppercase">Select Lesson:</span>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs font-medium text-slate-500">Language:</label>
          <select
            value={selectedLanguageId}
            onChange={(e) => setSelectedLanguageId(e.target.value)}
            className="px-3 py-1.5 rounded-xl border border-slate-300 text-xs font-semibold text-slate-800 bg-white"
          >
            {languages.map((l) => (
              <option key={l.id} value={l.id}>{l.flag} {l.name}</option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-2 flex-1 min-w-[200px]">
          <label className="text-xs font-medium text-slate-500">Lesson:</label>
          <select
            value={selectedLessonId}
            onChange={(e) => setSelectedLessonId(e.target.value)}
            className="w-full px-3 py-1.5 rounded-xl border border-slate-300 text-xs font-semibold text-slate-800 bg-white"
          >
            {langLessons.map((l) => (
              <option key={l.id} value={l.id}>
                #{l.lesson_order} - {l.title}
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* Vocabulary Cards Table */}
      {isLoading ? (
        <LoadingState message="Loading vocabulary words..." />
      ) : (
        <Card className="p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 text-slate-700 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-6">Word & Pronunciation</th>
                  <th className="py-3.5 px-6">Translation</th>
                  <th className="py-3.5 px-6">Example Sentence</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {vocabulary.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-4 px-6">
                      <p lang={selectedLang?.code || "en"} dir={selectedLang?.code === "ur" ? "rtl" : "ltr"} className="font-bold text-slate-900 text-sm font-devanagari">
                        {item.word}
                      </p>
                      {item.pronunciation && (
                        <p className="text-xs font-mono text-slate-400">
                          {item.pronunciation}
                        </p>
                      )}
                    </td>
                    <td className="py-4 px-6 font-semibold text-slate-800">
                      {item.translation}
                    </td>
                    <td className="py-4 px-6 max-w-xs">
                      {item.example_sentence && (
                        <div>
                          <p lang={selectedLang?.code || "en"} dir={selectedLang?.code === "ur" ? "rtl" : "ltr"} className="text-xs font-medium text-slate-700 font-devanagari">
                            "{item.example_sentence}"
                          </p>
                          {item.example_translation && (
                            <p className="text-[11px] text-slate-400 italic">
                              {item.example_translation}
                            </p>
                          )}
                        </div>
                      )}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button type="button" onClick={()=>handleOpenEdit(item)} className="text-xs text-brand-600 mr-3">Edit</button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setDeletingId(item.id);
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
                {vocabulary.length === 0 && (
                  <tr>
                    <td colSpan={5} className="py-12 text-center text-slate-400">
                      No vocabulary registered for this lesson. Click "Add Vocabulary Word" above.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Add Vocabulary Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingId?'Edit Vocabulary Word':'Add Vocabulary Word'}
      >
        <form onSubmit={handleFormSubmit} className="space-y-4">
          <ErrorMessage message={formError} />

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Target Word
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Bonjour or नमस्ते"
                value={formData.word}
                onChange={(e) => setFormData({ ...formData, word: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                English Translation
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Hello / Good day"
                value={formData.translation}
                onChange={(e) => setFormData({ ...formData, translation: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Pronunciation / Phonetic Guide (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. /bɔ̃.ʒuʁ/ or Namaste"
              value={formData.pronunciation}
              onChange={(e) => setFormData({ ...formData, pronunciation: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Example Sentence (Target Language)
            </label>
            <input
              type="text"
              placeholder="e.g. Bonjour tout le monde !"
              value={formData.example_sentence}
              onChange={(e) => setFormData({ ...formData, example_sentence: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Example Sentence Translation
            </label>
            <input
              type="text"
              placeholder="e.g. Good morning everyone!"
              value={formData.example_translation}
              onChange={(e) => setFormData({ ...formData, example_translation: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" isLoading={formSubmitting}>
              Save Vocabulary Item
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Vocabulary Word"
        message="Are you sure you want to remove this vocabulary item?"
      />
    </div>
  );
};
