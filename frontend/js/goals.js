// Goals module
const Goals = {
    currentGoals: [],

    init() {
        // Event listener attached via onclick in HTML for reliability
        console.log('[Goals] Init called');
    },

    async load() {
        try {
            UI.showLoading();
            this.currentGoals = await API.getGoals();
            this.render();
        } catch (error) {
            UI.showToast('Error loading goals', 'error');
            this.renderPlaceholder();
        } finally {
            UI.hideLoading();
        }
    },

    render() {
        const container = document.getElementById('goals-list');

        if (this.currentGoals.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No goals yet. Click "+ Add Goal" to create your first goal!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.currentGoals.map(goal => `
            <div class="item-card">
                <div class="item-header">
                    <h3>${goal.title}</h3>
                    <span class="badge badge-${goal.status}">${goal.status}</span>
                </div>
                <p>${goal.description || 'No description'}</p>
                <div class="item-meta">
                    <span>📅 ${goal.timeframe}</span>
                    <span>📊 ${goal.progress}% complete</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${goal.progress}%"></div>
                </div>
            </div>
        `).join('');
    },

    renderPlaceholder() {
        const container = document.getElementById('goals-list');
        container.innerHTML = `
            <div class="placeholder">
                <h3>Goals Feature</h3>
                <p>Track your short, medium, and long-term goals across all 8 life areas.</p>
                <p><strong>To add goals:</strong> Use the API at <a href="/docs" target="_blank">/docs</a> or we'll add a form here soon!</p>
            </div>
        `;
    },

    showAddForm() {
        const formHtml = `
            <div class="form-container">
                <h3>Add New Goal</h3>
                <form id="goal-form">
                    <div class="form-group">
                        <label for="goal-title">Title *</label>
                        <input type="text" id="goal-title" required placeholder="e.g., Run a 5K marathon">
                    </div>

                    <div class="form-group">
                        <label for="goal-description">Description</label>
                        <textarea id="goal-description" rows="3" placeholder="What does success look like?"></textarea>
                    </div>

                    <div class="form-group">
                        <label for="goal-timeframe">Timeframe *</label>
                        <select id="goal-timeframe" required>
                            <option value="">Select timeframe</option>
                            <option value="short">Short term (< 3 months)</option>
                            <option value="medium">Medium term (3-12 months)</option>
                            <option value="long">Long term (> 1 year)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="goal-target-date">Target Date</label>
                        <input type="date" id="goal-target-date">
                    </div>

                    <div class="form-group">
                        <label for="goal-progress">Current Progress (%)</label>
                        <input type="number" id="goal-progress" min="0" max="100" value="0">
                    </div>

                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="UI.hideModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">Create Goal</button>
                    </div>
                </form>
            </div>
        `;

        UI.showModal('Add Goal', formHtml);

        // Attach form submit handler
        document.getElementById('goal-form').addEventListener('submit', (e) => this.handleSubmit(e));
    },

    async handleSubmit(e) {
        e.preventDefault();

        const formData = {
            title: document.getElementById('goal-title').value,
            description: document.getElementById('goal-description').value || null,
            timeframe: document.getElementById('goal-timeframe').value,
            target_date: document.getElementById('goal-target-date').value || null,
            progress: parseInt(document.getElementById('goal-progress').value) || 0,
            status: 'active',
            area_ids: [1] // Default to first life area for now
        };

        try {
            UI.showLoading();
            await API.createGoal(formData);
            UI.hideModal();
            UI.showToast('Goal created successfully!', 'success');
            await this.load(); // Reload goals
        } catch (error) {
            UI.showToast(error.message || 'Failed to create goal', 'error');
        } finally {
            UI.hideLoading();
        }
    }
};
