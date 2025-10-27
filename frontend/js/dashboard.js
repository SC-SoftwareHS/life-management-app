// Dashboard module
const Dashboard = {
    async load() {
        try {
            UI.showLoading();
            const areas = await API.getLifeAreas();
            this.renderLifeAreas(areas);
        } catch (error) {
            UI.showToast('Error loading dashboard', 'error');
        } finally {
            UI.hideLoading();
        }
    },

    renderLifeAreas(areas) {
        const grid = document.getElementById('life-areas-grid');
        grid.innerHTML = areas.map(area => `
            <div class="life-area-card" onclick="Dashboard.selectArea('${area.name}')">
                <div class="icon">${area.icon || '📌'}</div>
                <h3>${area.display_name}</h3>
                <p>${area.description}</p>
            </div>
        `).join('');
    },

    selectArea(areaName) {
        // For now, just show a message
        // Later we can filter data by area
        UI.showToast(`Selected: ${areaName}`, 'success');

        // Navigate to relevant view based on area
        // For demo, let's go to goals
        this.showView('goals');
    },

    showView(viewName) {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => view.classList.add('hidden'));

        // Show selected view
        const viewId = `${viewName}-view`;
        const viewEl = document.getElementById(viewId);
        if (viewEl) {
            viewEl.classList.remove('hidden');

            // Load data for the view
            switch(viewName) {
                case 'goals':
                    if (window.Goals) {
                        Goals.init(); // Initialize event listeners
                        Goals.load();
                    }
                    break;
                case 'habits':
                    if (window.Habits) Habits.load();
                    break;
                case 'tasks':
                    if (window.Tasks) Tasks.load();
                    break;
                case 'contacts':
                    if (window.Contacts) Contacts.load();
                    break;
            }
        }
    },

    backToDashboard() {
        // Hide all views except dashboard
        document.querySelectorAll('.view').forEach(view => view.classList.add('hidden'));
        document.getElementById('dashboard-view').classList.remove('hidden');
    }
};
