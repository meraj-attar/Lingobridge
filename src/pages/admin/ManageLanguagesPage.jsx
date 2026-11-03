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
  Languages,
  Plus,
  Edit2,
  Trash2,
  CheckCircle2,
  XCircle,
  Sparkles,
  Globe
} from 'lucide-react';

export const ManageLanguagesPage = () => {
  const { refreshData } = useLearning();
  const [languages, setLanguages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modals state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentId, setCurrentId] = useState(null);

  // Form State
  const [formData, setFormData] = useState({
    name: '',
    native_name: '',
    code: '',
    flag: '🌐',
    description: '',
    is_active: true
  });
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  // Delete Dialog
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const fetchLanguages = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.getLanguages();
      setLanguages(data || []);
    } catch (err) {
      setError(err.message || 'Failed to load languages.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLanguages();
  }, []);

  const handleOpenAdd = () => {
    setFormData({
      name: '',
      native_name: '',
      code: '',
      flag: '🌐',
      description: '',
      is_active: true
    });
    setIsEditing(false);
    setCurrentId(null);
    setFormError('');
    setIsModalOpen(true);
  };

  const handleOpenEdit = (lang) => {
    setFormData({
      name: lang.name,
      native_name: lang.native_name,
      code: lang.code,
      flag: lang.flag || '🌐',
      description: lang.description || '',
      is_active: lang.is_active ?? true
    });
    setIsEditing(true);
    setCurrentId(lang.id);
    setFormError('');
    setIsModalOpen(true);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name || !formData.native_name || !formData.code) {
      setFormError('Name, native name, and language code are mandatory.');
      return;
    }

    try {
      setFormSubmitting(true);
      setFormError('');

      if (isEditing) {
        await api.updateLanguage(currentId, formData);
      } else {
        await api.createLanguage(formData);
      }

      setIsModalOpen(false);
      await fetchLanguages();
      await refreshData();
    } catch (err) {
      setFormError(err.message || 'Failed to save language.');
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleToggleActive = async (lang) => {
    try {
      await api.updateLanguage(lang.id, { is_active: !lang.is_active });
      await fetchLanguages();
      await refreshData();
    } catch (err) {
      setError(err.message || 'Failed to update status.');
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      await api.deleteLanguage(deletingId);
      setDeleteDialogOpen(false);
      setDeletingId(null);
      await fetchLanguages();
      await refreshData();
    } catch (err) {
      setError(err.message || 'Failed to delete language.');
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2">
            <Languages className="w-6 h-6 text-purple-600" />
            Manage Languages
          </h1>
          <p className="text-xs text-slate-500">
            Dynamically add or edit supported learning languages without code changes.
          </p>
        </div>

        <Button onClick={handleOpenAdd} variant="primary" size="sm" icon={Plus}>
          Add New Language
        </Button>
      </div>

      <ErrorMessage message={error} />

      {/* Languages Table */}
      {isLoading ? (
        <LoadingState message="Loading language records..." />
      ) : (
        <Card className="p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 text-slate-700 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-6">Language</th>
                  <th className="py-3.5 px-4">Code</th>
                  <th className="py-3.5 px-6">Description</th>
                  <th className="py-3.5 px-4 text-center">Status</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {languages.map((lang) => (
                  <tr key={lang.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{lang.flag || '🌐'}</span>
                        <div>
                          <p className="font-bold text-slate-900 text-sm">{lang.name}</p>
                          <p className="text-xs font-semibold text-slate-400 font-devanagari">
                            {lang.native_name}
                          </p>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4 font-mono font-bold text-slate-700 uppercase">
                      {lang.code}
                    </td>
                    <td className="py-4 px-6 max-w-xs truncate text-slate-500">
                      {lang.description || 'No description provided'}
                    </td>
                    <td className="py-4 px-4 text-center">
                      <button
                        onClick={() => handleToggleActive(lang)}
                        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold transition-colors ${
                          lang.is_active
                            ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200'
                            : 'bg-slate-100 text-slate-500 hover:bg-slate-200 border border-slate-200'
                        }`}
                      >
                        {lang.is_active ? 'Active' : 'Disabled'}
                      </button>
                    </td>
                    <td className="py-4 px-6 text-right space-x-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleOpenEdit(lang)}
                        icon={Edit2}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setDeletingId(lang.id);
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
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Add / Edit Language Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={isEditing ? 'Edit Language' : 'Add New Learning Language'}
      >
        <form onSubmit={handleFormSubmit} className="space-y-4">
          <ErrorMessage message={formError} />

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Language Name
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Japanese"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Native Name
              </label>
              <input
                type="text"
                required
                placeholder="e.g. 日本語 or हिन्दी"
                value={formData.native_name}
                onChange={(e) => setFormData({ ...formData, native_name: e.target.value })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-devanagari focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Language Code (ISO)
              </label>
              <input
                type="text"
                required
                placeholder="e.g. ja, it, ru"
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value.toLowerCase() })}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs font-mono focus:ring-2 focus:ring-purple-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Flag / Icon Emoji
              </label>
              <input
                type="text"
                required
                placeholder="e.g. 🇯🇵 or 🇮🇳"
                value={formData.flag}
                onChange={(e) => setFormData({ ...formData, flag: e.target.value })}
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
              placeholder="Brief overview of why learners should study this language..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500"
            />
          </div>

          <div className="flex items-center gap-2 pt-2">
            <input
              type="checkbox"
              id="is_active_check"
              checked={formData.is_active}
              onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
              className="rounded text-purple-600 focus:ring-purple-500"
            />
            <label htmlFor="is_active_check" className="text-xs font-semibold text-slate-700">
              Publish immediately (Active for all students)
            </label>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" isLoading={formSubmitting}>
              {isEditing ? 'Save Changes' : 'Create Language'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Language"
        message="Are you sure you want to delete this language? All associated lessons, vocabulary, and quizzes will also be removed."
      />
    </div>
  );
};
