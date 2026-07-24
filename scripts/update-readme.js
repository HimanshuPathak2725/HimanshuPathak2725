// scripts/update-readme.js
// Fetches live GitHub data and rewrites the section of README.md
// between <!-- LIVE-STATS:START --> and <!-- LIVE-STATS:END -->.

const fs = require('fs');

const USERNAME = process.env.GH_USERNAME || 'HimanshuPathak2725';
const TOKEN = process.env.GH_TOKEN;

const headers = {
  Authorization: `Bearer ${TOKEN}`,
  Accept: 'application/vnd.github+json',
  'User-Agent': USERNAME,
};

function timeAgo(date) {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  const intervals = [
    ['year', 31536000],
    ['month', 2592000],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
  ];
  for (const [name, secs] of intervals) {
    const count = Math.floor(seconds / secs);
    if (count >= 1) return `${count} ${name}${count > 1 ? 's' : ''} ago`;
  }
  return 'just now';
}

async function main() {
  const user = await fetch(`https://api.github.com/users/${USERNAME}`, { headers }).then(r => r.json());

  const events = await fetch(
    `https://api.github.com/users/${USERNAME}/events/public?per_page=30`,
    { headers }
  ).then(r => r.json());

  const pushEvent = Array.isArray(events) ? events.find(e => e.type === 'PushEvent') : null;

  let latestCommitMsg = 'No recent public commits found';
  let latestCommitRepo = '—';
  let latestCommitTime = '—';

  if (pushEvent) {
    const commits = pushEvent.payload.commits || [];
    const lastCommit = commits[commits.length - 1];
    if (lastCommit) latestCommitMsg = lastCommit.message.split('\n')[0];
    latestCommitRepo = pushEvent.repo.name;
    latestCommitTime = timeAgo(new Date(pushEvent.created_at));
  }

  const timestamp = new Date().toUTCString();

  const section = `
🟢 **Status:** Online — last synced ${timestamp}

📌 **Latest public activity:** \`${latestCommitMsg}\` in \`${latestCommitRepo}\` (${latestCommitTime})

📦 **Public repos:** ${user.public_repos ?? 'N/A'}   👥 **Followers:** ${user.followers ?? 'N/A'}

_This section refreshes automatically via GitHub Actions every 6 hours._
`;

  const readmePath = 'README.md';
  let readme = fs.readFileSync(readmePath, 'utf8');

  const startMarker = '<!-- LIVE-STATS:START -->';
  const endMarker = '<!-- LIVE-STATS:END -->';

  const startIdx = readme.indexOf(startMarker);
  const endIdx = readme.indexOf(endMarker);

  if (startIdx === -1 || endIdx === -1) {
    console.error(
      `Markers not found in README.md. Add ${startMarker} and ${endMarker} where you want the live section to appear.`
    );
    process.exit(1);
  }

  const newReadme =
    readme.slice(0, startIdx + startMarker.length) +
    '\n' + section + '\n' +
    readme.slice(endIdx);

  if (newReadme === readme) {
    console.log('No changes needed.');
    return;
  }

  fs.writeFileSync(readmePath, newReadme);
  console.log('README updated.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});