import { FORM_ERROR } from 'final-form';
import React from 'react';
import {Form as FinalForm, Field} from 'react-final-form';
import {isValidHttpUrl} from '../validators';

const FormComponent = ({handleSubmit, submitting, error}) => {
  return (
    <form
      className="link-form"
      onSubmit={(e) => {
        e.preventDefault();
      }}>
      {submitting ? 'Please, wait...' : 'Paste your link here' }
      <Field
        name="url"
        type="text"
        component="input"
        validate={isValidHttpUrl}>
        {({ meta, input }) => {
          return (
            <>
              <input {...input} onChange={(e) => {
                input.onChange(e.target.value);
                !submitting && handleSubmit();
              }} />
              <div style={{ color: 'red' }}>
                {!meta.pristine && meta.error}
              </div>
            </>
          );
        }}
      </Field>
      <div style={{ color: 'red' }}>
        {error}
      </div>
      <button
        disabled={submitting}
        onClick={handleSubmit}>
        Submit
      </button>
    </form>
  );
};

const Form = ({ onResult }) => {
  return (
    <div>
      <FinalForm
        component={FormComponent}
        onSubmit={async (form) => {
          const pathname = new URL(form?.url).pathname || "";

          const id = pathname.split('/status/')[1];
          if(!id) {
            return {
              [FORM_ERROR]: 'Wrong link format'
            }
          }
          const response = await fetch('http://localhost:5000/', {
            method: 'POST',
            body: JSON.stringify({ id }),
            headers: {
              'content-type': 'application/json'
            }
          });
          const data = await response.json();
          onResult(data);
        }} />
    </div>
  )
};

export default Form;