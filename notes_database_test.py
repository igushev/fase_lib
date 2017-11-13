import datetime
import os
import signal
import subprocess
import unittest

import notes_database
import notes_model


DYNAMODB_CMD = (
    'java'
    ' -Djava.library.path=~/DynamoDBLocal/DynamoDBLocal_lib'
    ' -jar ~/DynamoDBLocal/DynamoDBLocal.jar -inMemory')


class DynamoDBNotesDatabaseTest(unittest.TestCase):

  def setUp(self):
    super(DynamoDBNotesDatabaseTest, self).setUp()
    self.dynamodb_process = (
        subprocess.Popen(DYNAMODB_CMD, shell=True, preexec_fn=os.setsid))
    notes_database.NotesDatabaseInterface.Set(
        notes_database.DynamoDBNotesDatabase(region_name='us-west-2',
                                             endpoint_url='http://localhost:8000',
                                             aws_access_key_id='Notes',
                                             aws_secret_access_key='Notes'),
        overwrite=True)

  def tearDown(self):
    os.killpg(self.dynamodb_process.pid, signal.SIGKILL)
    super(DynamoDBNotesDatabaseTest, self).tearDown()

  def testNotes(self):
    notes_database.NotesDatabaseInterface.Get().CreateTables()
    datetime_now = datetime.datetime.now()
    note_1_1 = notes_model.Note(note_id='321_1',
                                user_id='321',
                                header='Note 1 Header',
                                text='Note 1 text',
                                datetime=datetime_now+datetime.timedelta(days=1),
                                favourite=False)
    note_1_2 = notes_model.Note(note_id='321_2',
                                user_id='321',
                                header='Note 2 Header',
                                text='Note 2 text',
                                datetime=datetime_now-datetime.timedelta(days=1),
                                favourite=True)
    note_1_2_edited = notes_model.Note(note_id='321_2',
                                       user_id='321',
                                       header='Note 2 Header edited',
                                       text='Note 2 text edited',
                                       datetime=datetime_now-datetime.timedelta(days=1),
                                       favourite=True)
    note_1_3 = notes_model.Note(note_id='321_3',
                                user_id='321',
                                header='Note 3 Header',
                                text='Note 3 text',
                                datetime=datetime_now,
                                favourite=False)
    note_2_1 = notes_model.Note(note_id='456_1',
                                user_id='456',
                                header='Note 1 Header',
                                text='Note 1 text',
                                datetime=datetime_now+datetime.timedelta(days=1),
                                favourite=False)
    note_2_2 = notes_model.Note(note_id='456_2',
                                user_id='456',
                                header='Note 2 Header',
                                text='Note 2 text',
                                datetime=datetime_now-datetime.timedelta(days=1),
                                favourite=True)
    note_2_3 = notes_model.Note(note_id='456_3',
                                user_id='456',
                                header='Note 3 Header',
                                text='Note 3 text',
                                datetime=datetime_now,
                                favourite=False)
    # Before adding any notes.
    self.assertRaises(KeyError, notes_database.NotesDatabaseInterface.Get().GetNote, note_1_1.note_id)
    self.assertEqual([],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))
    # Add note_1_1.
    notes_database.NotesDatabaseInterface.Get().AddNote(note_1_1)
    self.assertEqual(note_1_1,
                     notes_database.NotesDatabaseInterface.Get().GetNote(note_1_1.note_id))
    self.assertEqual([note_1_1],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))
    # Add note_1_2.
    notes_database.NotesDatabaseInterface.Get().AddNote(note_1_2)
    self.assertEqual(note_1_2,
                     notes_database.NotesDatabaseInterface.Get().GetNote(note_1_2.note_id))
    self.assertEqual([note_1_2, note_1_1],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))
    # Add note_1_3.
    notes_database.NotesDatabaseInterface.Get().AddNote(note_1_3)
    self.assertEqual(note_1_3,
                     notes_database.NotesDatabaseInterface.Get().GetNote(note_1_3.note_id))
    self.assertEqual([note_1_2, note_1_3, note_1_1],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))

    # Replace note_1_2 with note_1_2_edited
    notes_database.NotesDatabaseInterface.Get().AddNote(note_1_2_edited)
    self.assertEqual(note_1_2_edited,
                     notes_database.NotesDatabaseInterface.Get().GetNote(note_1_2.note_id))
    self.assertEqual([note_1_2_edited, note_1_3, note_1_1],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))
    
    # Add notes for other user.
    notes_database.NotesDatabaseInterface.Get().AddNote(note_2_1)
    notes_database.NotesDatabaseInterface.Get().AddNote(note_2_2)
    notes_database.NotesDatabaseInterface.Get().AddNote(note_2_3)

    # Assert that data for first user is OK.
    self.assertEqual([note_1_2_edited, note_1_3, note_1_1],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))

    # Delete note_1_3
    notes_database.NotesDatabaseInterface.Get().DeleteNote(note_1_3.note_id)
    self.assertRaises(KeyError, notes_database.NotesDatabaseInterface.Get().GetNote, note_1_3.note_id)
    self.assertEqual([note_1_2_edited, note_1_1],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))

    # Delete note_1_1
    notes_database.NotesDatabaseInterface.Get().DeleteNote(note_1_1.note_id)
    self.assertRaises(KeyError, notes_database.NotesDatabaseInterface.Get().GetNote, note_1_1.note_id)
    self.assertEqual([note_1_2_edited],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))

    # Delete note_1_2
    notes_database.NotesDatabaseInterface.Get().DeleteNote(note_1_2.note_id)
    self.assertRaises(KeyError, notes_database.NotesDatabaseInterface.Get().GetNote, note_1_2.note_id)
    self.assertEqual([],
                     notes_database.NotesDatabaseInterface.Get().GetUserNotes(note_1_1.user_id))



if __name__ == '__main__':
    unittest.main()
