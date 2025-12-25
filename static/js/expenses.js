async function api(url, method='GET', body) {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if(token) headers['Authorization'] = 'Token ' + token;
  const res = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : undefined });
  return res.json();
}

async function loadExpenses(){
  const list = document.getElementById('list');
  list.textContent='Loading...';
  try{
    const data = await api('/api/expenses/');
    if(Array.isArray(data)){
      list.innerHTML = data.map(e => `<div><strong>${e.amount}</strong> - ${e.description || ''} <em>${e.date}</em></div>`).join('');
      renderChart(data);
    }else{
      list.textContent = JSON.stringify(data);
    }
  }catch(e){ list.textContent = String(e) }
}

function renderChart(data){
  const sums = {};
  data.forEach(d => { const cat = (d.category && d.category.name) || 'Uncategorized'; sums[cat] = (sums[cat] || 0) + parseFloat(d.amount); });
  const ctx = document.getElementById('chart').getContext('2d');
  if(window._chart) window._chart.destroy();
  window._chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(sums),
      datasets: [{ data: Object.values(sums), backgroundColor: ['#0ee3a1', '#07b58f', '#04785b', '#023f2e'] }]
    }
  });
}

document.getElementById('add-expense')?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const form = e.target;
  const body = { amount: parseFloat(form.amount.value), description: form.description.value, date: form.date.value || new Date().toISOString().slice(0,10) };
  const res = await api('/api/expenses/', 'POST', body);
  await loadExpenses();
});

loadExpenses();
