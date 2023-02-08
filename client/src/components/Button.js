import styled from "styled-components";

const Button = styled.button`
  border-radius: 3px;
  color: white;
  cursor: pointer;
  padding: 1em;
  border: none;
  font-size: 1em;
  transition: ease-in-out 0.1s all;
`

export const MainButton = styled(Button)`
  background-color: ${props => props.theme.main};
  
  &:hover {
    background-color: ${props => props.theme.hoverMain};
  }
`

export const SecondaryButton = styled(Button)`
  background-color: ${props => props.theme.secondary};
`
