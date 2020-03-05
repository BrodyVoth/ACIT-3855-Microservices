import React from 'react'
import { render } from '@testing-library/react'
import Quote from './index'

const quote = "Perhaps I should have been more like water today"

test('Renders the quote', () => {
  let { queryByText } = render(<Quote quote={quote} />)
  let quoteElement = queryByText(quote) 
  expect(quoteElement).toBeInTheDocument()
})

test('Renders the quoter', () => {
  let { queryByText } = render(<Quote quote={quote} quoter={"Kanye"} />)
  let quoteElement = queryByText("Kanye") 
  expect(quoteElement).toBeInTheDocument()
})