import React, { useEffect, useState } from 'react';
import { Table, Card, Form, Button, Alert } from 'react-bootstrap';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [form, setForm] = useState({ id: '', team: '', total_points: '' });
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const endpoint = `${process.env.REACT_APP_CODESPACE_NAME ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev` : 'http://localhost:8000'}/api/leaderboards/`;

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaderboard(results);
        console.log('Leaderboard endpoint:', endpoint);
        console.log('Fetched leaderboard:', results);
      });
  }, [endpoint, success]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSuccess('');
    setError('');
    // Team must be a valid team id
    fetch(`${process.env.REACT_APP_CODESPACE_NAME ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev` : 'http://localhost:8000'}/api/teams/${form.team}/`)
      .then(res => {
        if (!res.ok) throw new Error('Team not found');
        return res.json();
      })
      .then(teamObj => {
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: form.id,
            team: teamObj.id,
            total_points: form.total_points
          })
        })
        .then(res => {
          if (!res.ok) throw new Error('Failed to add leaderboard entry');
          return res.json();
        })
        .then(data => {
          setSuccess('Leaderboard entry added!');
          setForm({ id: '', team: '', total_points: '' });
        })
        .catch(err => setError(err.message));
      })
      .catch(err => setError(err.message));
  };

  return (
    <Card className="mt-4">
      <Card.Header as="h2" className="bg-success text-white">Leaderboard</Card.Header>
      <Card.Body>
        <Form onSubmit={handleSubmit} className="mb-4">
          <Form.Group className="mb-2" controlId="formId">
            <Form.Label>ID</Form.Label>
            <Form.Control type="text" name="id" value={form.id} onChange={handleChange} required />
          </Form.Group>
          <Form.Group className="mb-2" controlId="formTeam">
            <Form.Label>Team ID</Form.Label>
            <Form.Control type="text" name="team" value={form.team} onChange={handleChange} required placeholder="Enter Team ID" />
          </Form.Group>
          <Form.Group className="mb-2" controlId="formPoints">
            <Form.Label>Total Points</Form.Label>
            <Form.Control type="number" name="total_points" value={form.total_points} onChange={handleChange} required />
          </Form.Group>
          <Button type="submit" className="mt-2">Add Leaderboard Entry</Button>
        </Form>
        {success && <Alert variant="success">{success}</Alert>}
        {error && <Alert variant="danger">{error}</Alert>}
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>ID</th>
              <th>Team</th>
              <th>Total Points</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map(entry => (
              <tr key={entry.id}>
                <td>{entry.id}</td>
                <td>{entry.team?.name || entry.team}</td>
                <td>{entry.total_points}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
};

export default Leaderboard;
