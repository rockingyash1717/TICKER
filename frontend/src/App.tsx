import styled from '@emotion/styled'
import { ChatBox } from './components/ChatBox'

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #f7fafc;
  padding: 40px 20px;
`

const Title = styled.h1`
  text-align: center;
  color: #2d3748;
  margin-bottom: 40px;
  font-size: 2.5rem;
`

function App() {
  return (
    <AppContainer>
      <Title>Market Pulse Chat</Title>
      <ChatBox />
    </AppContainer>
  )
}

export default App
