import express from 'express';
import cors from 'cors';
import { Pool } from 'pg';

const app = express();
const port = 5000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

app.use(cors());
app.use(express.json());

// Schema Design Routes
app.post('/schemas', async (req, res) => {
  try {
    const { name, tables } = req.body;
    // Save schema to database
    const result = await pool.query(
      'INSERT INTO schemas (name, tables) VALUES ($1, $2) RETURNING *', 
      [name, JSON.stringify(tables)]
    );
    res.json(result.rows[0]);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create schema' });
  }
});

app.get('/schemas', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM schemas');
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve schemas' });
  }
});

app.listen(port, () => {
  console.log(`Schema Designer Backend running on port ${port}`);
});
