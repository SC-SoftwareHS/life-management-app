// Goals module
const Goals = {
    currentGoals: [],

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
    }
};
