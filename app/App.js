/* @flow */
import * as React from 'react'
import { hot } from 'react-hot-loader'

import './App.scss'

// API url
const API_URL = '/api/neo4j-driver'

// default query
const CQL = `
MATCH (actor:Person {name: 'Bill Paxton'})-[:ACTED_IN]->(movie)<-[:DIRECTED]-(director)
RETURN actor,movie,director
LIMIT 10
`.trim()

type Props = {}

type State = {
  query: string,
  response: ?string,
  responseError: ?string,
  submitting: boolean,
}

export class App extends React.Component<Props, State> {
  state = {
    query: CQL,
    response: null,
    responseError: null,
    submitting: false,
  }

  submitForm = (e: Event) => {
    e.preventDefault()
    const { query } = this.state

    this.setState({ response: null, responseError: null })

    if (!query) return

    this.setState({ submitting: true })

    // Use fetch api to send post with CQL query as request body
    fetch(API_URL, { method: 'POST', body: query })
      .then((response) => {
        this.setState({ submitting: false })

        const isError = response.status >= 300
        const stateVar = isError ? 'response' : 'responseError'
        const contentType = response.headers.get('content-type')
        const isJson = contentType.indexOf('application/json') !== -1

        if (isJson) {
          response.json().then((json) => {
            this.setState({
              [stateVar]: JSON.stringify(json, null, 2),
            })
          })
        }
        else {
          response.text().then((text) => {
            this.setState({
              [stateVar]: text,
            })
          })
        }
      })
      .catch((error) => {
        this.setState({
          submitting: false,
          responseError: error.toString(),
        })
      })
  }

  handleQueryChange = (e: any) => {
    this.setState({ query: e.target.value })
  }

  render() {
    const { response, responseError, submitting } = this.state
    return (
      <div className="App">
        <h1>Graphene/Neo4j &amp; Django Test</h1>

        <p>
          The <a href="https://github.com/neo4j/neo4j-python-driver">neo4j-driver</a> python
          package is used to connect to Graphenedb.
          <br />
          Django/Python acts a light wrapper for passing through CQL queries.
        </p>

        <ol>
          <li>
            Django view receives CQL query via POST.
          </li>
          <li>
            Query is sent to Graphenedb using BOLT protocol.
          </li>
          <li>
            JSON responses are generated using&nbsp;
            <a href="http://www.django-rest-framework.org/">django-rest-framework</a> and
            returned to the client.
          </li>
          <li>
            Errors return a HTTP 400 response to the client with the neo4j error message.
          </li>
          <li>
            Authentication is handled server-side without exposing graphenedb
            credentials to the client.
          </li>
          <li>
            The client app is free to send any CQL queries to graphenedb.
          </li>
        </ol>

        <form className="App__query-form" onSubmit={this.submitForm}>
          <label htmlFor="query-input">Enter a Cypher query:</label>
          <textarea
            id="query-input"
            rows="7"
            value={this.state.query}
            onChange={this.handleQueryChange}
          />

          <button>{ submitting ? 'Submitting...' : 'Submit' }</button>
        </form>

        {response && (
          <div>
            <label>Response:</label>
            <pre>{response}</pre>
          </div>
        )}

        {responseError && (
          <div>
            <label>Response Error:</label>
            <pre>{responseError}</pre>
          </div>
        )}
      </div>
    )
  }
}

export default hot(module)(App)
