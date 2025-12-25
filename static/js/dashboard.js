async function postJSON(url, body) {
  const token = localStorage.getItem('token');
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? ('Token ' + token) : ''
    },
    body: JSON.stringify(body)
  });
  return res.json();
}

document.getElementById('suggest')?.addEventListener('click', async () => {
  const out = document.getElementById('ai-output');
  out.textContent = 'Thinking...';
  try {
    const res = await postJSON('/api/ai/suggest-budget/', { months_of_history: 3 });
    out.textContent = JSON.stringify(res, null, 2);
  } catch (e) {
    out.textContent = String(e);
  }
});

document.getElementById('forecast')?.addEventListener('click', async () => {
  const out = document.getElementById('ai-output');
  out.textContent = 'Forecasting...';
  try {
    const res = await postJSON('/api/ai/forecast/', { months: 3 });
    out.textContent = JSON.stringify(res, null, 2);
  } catch (e) {
    out.textContent = String(e);
  }
});
